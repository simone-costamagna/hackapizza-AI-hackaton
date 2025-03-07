import logging
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from neo4j import GraphDatabase
from knowledge_base.vector_db.rag_utils import search

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_DB = os.getenv("NEO4J_DB")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

neo4j_driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


def to_lowercase(match):
    return f"{match.group(1)}{match.group(2).lower()}{match.group(3)}"


@tool
def retrieve_functional_context(question: str, k: int) -> str:
    """
    Tool che esegue un processo di Retrieval-Augmented Generation (RAG) per recuperare informazioni non strutturate
    da una base di conoscenza composta dai seguenti documenti:

    - Manuale di Cucina di Sirius Cosmo: Include informazioni su licenze richieste, Ordini della Galassia, elenco e descrizioni di Tecniche di preparazione,
      cottura e tecniche avanzate.
    - Blog: Contiene recensioni da parte dei clienti.
    - Codice Galattico: Fornisce dettagli su definizione degli ordini, sostanze regolamentate, limiti quantitativi,
      licenze, tecniche di preparazione e sanzioni.

    Args:
        question (str): La domanda o query per cui cercare informazioni rilevanti nel database vettoriale.
        k (int): Il numero massimo di chunks pertinenti da recuperare dal database vettoriale.

    Returns:
        str: I chunks di contesto recuperati, concatenati e formattati come stringa.
    """
    def search_functional_context(question, k):
        logging.info(f'Tool "functional context" - VectorDb tool has been invoked - Question: {question}; k: {k}')

        chunks = search(question, k)

        context = 'Vector DB content:\n'
        for index, document in enumerate(chunks):
            # Append the page_content to the combined string with a separator
            context += f"{index+1}) {document.page_content.lower()}\n"
        context += "\n"

        logging.debug(f"Tools Functional Context - Vector Db tool output: {context}")
        logging.info(f"Tools Functional Context - Vector Db tool finished - {len(chunks)} chunks retrieved.")

        return context

    return search_functional_context(question, k)


@tool
def retrieve_technical_context(query_cypher: str) -> str:
    """
    Tool che esegue una query cypher su un database a grafo per recuperare informazioni strutturate
    da una base di conoscenza.\n

    Args:
        query_cypher (str): Query Cypher da eseguire sul database. I nomi propri devono essere in minuscolo con LOWER()

    Returns:
        str: Risultato della query formattato come stringa leggibile.
    """
    def search_technical_context(query):
        logging.info(f'Tool "technical context" - GraphDb tool has been invoked - Query: {query}')

        results = []
        try:
            with neo4j_driver.session() as session:
                query_results = session.run(query)
                for record in query_results:
                    results.append(record.data())
        except Exception as e:
            logging.error(f"An error occurred while executing the query: {e}")
            return f"Error: invalid query cypher: {str(e)}"

        context = 'Graph DB content:\n'
        for index, result in enumerate(results):
            # Append the page_content to the combined string with a separator
            context += f"{index+1}) {result}\n"
        context += "\n"

        logging.debug(f"Tools Technical Context - Graph Db output: {results}")
        logging.info(f"Tools Technical Context - Graph Db tool finished - {len(results)} results retrieved.")

        return context

    return search_technical_context(query_cypher)


tools = [retrieve_functional_context, retrieve_technical_context]