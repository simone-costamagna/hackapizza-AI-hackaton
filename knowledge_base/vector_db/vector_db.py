import logging
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from tqdm import tqdm
from knowledge_base.config import VECTOR_DB
from knowledge_base.vector_db.db_utils import create_tables
from knowledge_base.vector_db.rag_utils import loader

load_dotenv()


def setup(status):
    create_tables()


def load_documents(status):
    logging.info(f"Loading vector db documents started")

    for file in tqdm(status['files'][VECTOR_DB], desc="Loading documents"):
        loader(file[0])

    logging.info(f"Documents loaded.")

    return status


vector_db = (
    RunnablePassthrough(setup)
    | RunnablePassthrough(load_documents)
)