import os

from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough

from config import DATA_FOLDER_PATH, OUTPUT_FOLDER, OUTPUT_PREPROCESSING_FOLDER, OUTPUT_PREPROCESSING_MD_FILES_FOLDER, \
    OUTPUT_JSON_TEMPLATES_FOLDER, OUTPUT_JSON_TEMPLATE_FOLDER
from preprocessing.abstract_entity_extractor.abstract_entity_extractor import abstract_entity_extractor
from preprocessing.parser.parser import parser
from log_config.log_config import setup_logging

load_dotenv()

setup_logging()

input = {
    'data_folder_path': DATA_FOLDER_PATH,
}

def setup(status):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_PREPROCESSING_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_PREPROCESSING_MD_FILES_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_JSON_TEMPLATES_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_JSON_TEMPLATE_FOLDER, exist_ok=True)


chain = (
    RunnablePassthrough(setup)
    | parser
    | abstract_entity_extractor
)

res = chain.invoke(input)


