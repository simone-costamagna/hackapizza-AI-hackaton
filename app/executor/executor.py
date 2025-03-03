import logging
import os
from langchain_core.runnables import RunnablePassthrough
from app.agent import Agent
from app.researcher.graph_researcher import graph_researcher
from config import OUTPUT_KB_GRAPH_SCHEMA, OUTPUT_APP


def log(status):
    logging.info(f"Agent 'executor risposte: {status['responses']}")


def setup():
    file_path = os.path.join(OUTPUT_KB_GRAPH_SCHEMA, 'schema.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        schema = file.read()

    os.makedirs(OUTPUT_APP, exist_ok=True)

    return schema, []


def invoke_graph_researcher(status):
    responses = []

    schema, output = setup()
    for question in status["questions"]:
        response = graph_researcher.invoke({
            "messages": ("user", question),
            "schema": schema,
            "output": output
        })
        responses.append(response['messages'][-1].content)

    return responses


chain = (
    RunnablePassthrough.assign(responses=invoke_graph_researcher)
    | RunnablePassthrough(log)
)

executor = Agent("executor", chain)

