import os
from config import MENU_FOLDER_PATH, MISC_FOLDER_PATH, OUTPUT_PREPROCESSING_MD_FILES_FOLDER, OUTPUT_JSON_TEMPLATE_FOLDER

TEMPLATE = "Template"
GRAPH_DB = "Graph db"
VECTOR_DB = "Vector db"

CLASSES = {
    TEMPLATE: [os.path.join(OUTPUT_JSON_TEMPLATE_FOLDER, 'template.json')],
    GRAPH_DB: [MENU_FOLDER_PATH, os.path.join(MISC_FOLDER_PATH, 'Distanze.csv')],
    VECTOR_DB: [OUTPUT_PREPROCESSING_MD_FILES_FOLDER]
}

EXAMPLE_PATH = 'knowledge_base/graph_db/example.txt'