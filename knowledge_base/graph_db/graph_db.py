import csv
import json
import logging
import os
from langchain_core.runnables import RunnablePassthrough
from tqdm import tqdm
from config import OUTPUT_KB_ENTITIES_FOLDER
from knowledge_base.config import GRAPH_DB, TEMPLATE
from knowledge_base.graph_db.prompts import PROMPT_EXTRACT_ENTITY
from utils.wrapper import LLMWrapper

wrapper = LLMWrapper()
wrapper.activate_json_mode()

runnable_get_json_templates = (
    PROMPT_EXTRACT_ENTITY | wrapper.llm | wrapper.parser
)


def extract_entity(status):
    logging.info(f"Extracting entities using json template")

    graph_db_entites = []

    template = status['files'][TEMPLATE][0][1]
    for file in tqdm(status['files'][GRAPH_DB], desc="Extracting json entities from files"):
        file_name = os.path.basename(file[0])

        if file_name != 'Distanze.csv':
            entity_json_file_path = os.path.join(OUTPUT_KB_ENTITIES_FOLDER, os.path.splitext(file_name)[0] + '.json')
            if os.path.exists(entity_json_file_path):
                with open(entity_json_file_path, 'r', encoding='utf-8') as json_file:
                    entities = json_file.read()
            else:
                input = {
                    "template": template,
                    "documento": file[1]
                }

                entities = runnable_get_json_templates.invoke(input)

                with open(entity_json_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(entities, json_file, ensure_ascii=False, indent=4)

            graph_db_entites.append(entities)
        else:
            entity_json_file_path = os.path.join(OUTPUT_KB_ENTITIES_FOLDER, os.path.splitext(file_name)[0] + '.csv')
            with open(entity_json_file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(file[1])

    logging.info(f"Entities extracted.")

    return graph_db_entites


graph_db = (
    RunnablePassthrough.assign(entities=extract_entity)
)