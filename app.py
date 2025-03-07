import csv
import itertools
import logging
import os
import sys

from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
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

    return status

chain = (
    graph
)

with open(DOMANDE_PATH, mode='r', encoding='utf-8') as csv_file:
    csv_questions = list(csv.reader(csv_file))

    responses = [["row_id", "result"]]
    start = 81
    for index, question in enumerate(csv_questions[start:]):
        try:
            logging.info(f"Started answering num {index + start}: {question[0]}")
            response = chain.invoke({"main_question": question[0]})
            if len(response['final_response']) > 0:
                result = ",".join(str(val) for val in response['final_response'])
                responses.append([index + 1, result])
            else:
                responses.append([index + 1, "50"])
        except Exception as e:
            logging.error(f"Error for question {question} at index {index}: {e}")
            responses.append([index + 1, "50"])

        logging.info(f"Final response: {responses[-1][1]}\n-----------------------------------------------------------------------------------------------------------------------\n")

    # Save output
    with open(OUTPUT_DOMANDE, mode='w', encoding='utf-8', newline='') as csv_file_output:
        # Create a custom dialect for selective quoting
        class CustomDialect(csv.excel):
            quoting = csv.QUOTE_NONE
            quotechar = '"'
            delimiter = ','

        writer = csv.writer(csv_file_output, dialect=CustomDialect)

        # Write header
        writer.writerow(responses[0])

        for row in responses[1:]:
            formatted_row = [str(row[0]), f'"{row[1]}"']
            csv_file_output.write(f"{formatted_row[0]},{formatted_row[1]}\n")
