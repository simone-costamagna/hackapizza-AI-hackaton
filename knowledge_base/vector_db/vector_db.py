import csv
import json
import logging
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_neo4j import Neo4jVector
from neo4j import GraphDatabase
from tqdm import tqdm
from config import OUTPUT_KB_ENTITIES_FOLDER
from knowledge_base.config import GRAPH_DB, TEMPLATE, VECTOR_DB
from knowledge_base.graph_db.prompts import PROMPT_EXTRACT_ENTITY
from knowledge_base.vector_db.rag_utils import loader
from utils.wrapper import LLMWrapper, EmbeddingWrapper

load_dotenv()


def load_documents(status):
    logging.info(f"Loading vector db documents started")

    for file in tqdm(status['files'][VECTOR_DB], desc="Loading documents"):
        loader(file[0])

    logging.info(f"Documents loaded.")

    return status


vector_db = (
    RunnablePassthrough(load_documents)
)