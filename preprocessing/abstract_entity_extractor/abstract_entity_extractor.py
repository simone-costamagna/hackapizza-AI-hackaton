import logging
from langchain_core.runnables import RunnablePassthrough
from tqdm import tqdm

from config import FOOD_CONTENT, CONTESTO

runnable_get_json_templates = (
    RunnablePassthrough.assign()
)


def get_json_templates(input):
    logging.info("Getting json template for each file...")

    files = input['files']

    templates = []
    for file in tqdm(files[FOOD_CONTENT], desc="File elaboration"):
        status = {
            'documento': file[1],
            'contesto': CONTESTO
        }
        template = runnable_get_json_templates.invoke(status)
        templates.append(template)

    logging.info(f"Process files completed. Json templates obtained: {len(templates)}")

    return templates


abstract_entity_extractor = (
    RunnablePassthrough.assign(
        json_templates=get_json_templates
    )
)