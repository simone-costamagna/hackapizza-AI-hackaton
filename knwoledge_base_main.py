import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from config import OUTPUT_KB_FOLDER, OUTPUT_KB_ENTITIES_FOLDER, OUTPUT_KB_GRAPH_SCHEMA
from knowledge_base.graph_db.graph_db import graph_db
from knowledge_base.loader.loader import loader
from knowledge_base.vector_db.vector_db import vector_db
from log_config.log_config import setup_logging

load_dotenv()

setup_logging()


def setup(status):
    os.makedirs(OUTPUT_KB_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_KB_ENTITIES_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_KB_GRAPH_SCHEMA, exist_ok=True)

chain = (
    RunnablePassthrough(setup)
    | loader
    | graph_db
    | vector_db
)

res = chain.invoke({})


