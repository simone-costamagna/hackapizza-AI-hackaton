import json
import logging
import os

from langchain_core.runnables import RunnablePassthrough
from tqdm import tqdm
from config import CONTESTO, OUTPUT_JSON_TEMPLATES_FOLDER, OUTPUT_JSON_TEMPLATE_FOLDER
from preprocessing.abstract_entity_extractor.prompts import PROMPT_EXTRACT_ENTITY, ABSTRACT_JSON_TEMPLATE, \
    PROMPT_JSON_TEMPLATES, PROMPT_CLEANER_TEMPLATE
from preprocessing.config import RESOURCES
from utils.wrapper import LLMWrapper

wrapper = LLMWrapper()
wrapper.activate_json_mode()

runnable_get_json_templates = (
    PROMPT_EXTRACT_ENTITY | wrapper.llm | wrapper.parser
)

runnable_json_templates = (
    PROMPT_JSON_TEMPLATES | wrapper.llm | wrapper.parser
)

runnable_clean_json_template = (
    PROMPT_CLEANER_TEMPLATE | wrapper.llm | wrapper.parser
)


def get_json_templates(status):
    logging.info("Getting json template for each file...")

    files = status['files']

    templates = []
    for file in tqdm(files[RESOURCES], desc="Getting json template from files"):
        file_name = os.path.basename(file[0])

        if not "Distanze.csv" == file_name:
            json_file_path = os.path.join(OUTPUT_JSON_TEMPLATES_FOLDER, os.path.splitext(file_name)[0] + '.json')

            if os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    template = json_file.read()
            else:
                input = {
                    'documento': file[1],
                    'contesto': CONTESTO,
                    'abstract_json_template': ABSTRACT_JSON_TEMPLATE
                }
                template = runnable_get_json_templates.invoke(input)

                with open(json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(template, json_file, ensure_ascii=False, indent=4)

            templates.append(template)


    logging.info(f"Process files completed. Json templates obtained: {len(templates)}")

    return templates


def process_templates(status):
    logging.info(f"Process schema started, templates: {len(status['json_templates'])}")

    json_file_path = os.path.join(OUTPUT_JSON_TEMPLATE_FOLDER, 'row_template.json')
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            return json_file.read()
    else:
        json_templates = []

        for i in tqdm(range(0, len(status['json_templates']), 5), desc="Merging templates"):
            blocks = status['json_templates'][i:i + 5]
            templates_content = ""
            for block in blocks:
                templates_content += f"Template:\n{block}\n\n"

            template = runnable_json_templates.invoke({"json_templates": templates_content})
            json_templates.append(template)

        if len(json_templates) == 1:
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_templates[0], json_file, ensure_ascii=False, indent=4)

            logging.info(f"Process json templates completed.")
            return json_templates[0]
        else:
            return process_templates({'json_templates': json_templates})


def clean_template(status):
    logging.info(f"Cleaning schema started")

    cleaned_json_file_path = os.path.join(OUTPUT_JSON_TEMPLATE_FOLDER, 'cleaned_template.json')
    if os.path.exists(cleaned_json_file_path):
        with open(cleaned_json_file_path, 'r', encoding='utf-8') as json_file:
            return json_file.read()
    else:
        input = {
            "contesto": CONTESTO,
            "json_template": status["template"]
        }
        template = runnable_clean_json_template.invoke(input)

        with open(cleaned_json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(template, json_file, ensure_ascii=False, indent=4)

        logging.info(f"Json template cleaned.")

        return template


abstract_entity_extractor = (
    RunnablePassthrough.assign(
        json_templates=get_json_templates
    )
    | RunnablePassthrough.assign(
        template=process_templates
    )
    | RunnablePassthrough.assign(
        template=clean_template
    )
)