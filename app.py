import csv
import logging
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from tqdm import tqdm

from app.graph import graph
from config import OUTPUT_KB_GRAPH_SCHEMA, OUTPUT_APP, OUTPUT_DOMANDE, DOMANDE_PATH
from log_config.log_config import setup_logging

load_dotenv()

setup_logging()


def setup(status):
    file_path = os.path.join(OUTPUT_KB_GRAPH_SCHEMA, 'schema.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        schema = file.read()

    status['schema'] = schema
    status['output'] = []

    os.makedirs(OUTPUT_APP, exist_ok=True)
    os.makedirs(OUTPUT_DOMANDE, exist_ok=True)

    return status


chain = (
    RunnablePassthrough(setup)
    | graph
)

with open(DOMANDE_PATH, mode='r', encoding='utf-8') as csv_file:
    csv_question = csv.reader(csv_file)

    next(csv_question)

    responses = [["row_id", "result"]]
    for index, question in tqdm(enumerate(csv_question), desc="Answering questions..."):
        try:
            response = chain.invoke({"messages": ("user", question[0])})
            if len(response['output']) > 0:
                result = ",".join(map(str, response['output']))
            else:
                result = "50"
            responses.append([index+1, result])
        except Exception as e:
            logging.error(f"Error for question {question} at index {index}: {e}")
            responses.append([index, "[50]"])  # Gestione degli errori

    with open(OUTPUT_DOMANDE, mode='w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(responses)
