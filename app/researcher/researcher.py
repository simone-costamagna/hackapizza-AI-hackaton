import logging
from langchain_core.runnables import RunnablePassthrough
from app.researcher.agent import Agent
from app.researcher.examples import examples
from app.researcher.prompts import prompt_researcher
from utils.wrapper import LLMWrapper
from app.researcher.tools.tools import retrieve_functional_context, retrieve_technical_context

wrapper = LLMWrapper()
wrapper.bind_tools([retrieve_functional_context, retrieve_technical_context])


def add_examples(status):
    return examples


def log_input(input):
    logging.info(f"Agent 'researcher' - Question: {input['messages'][-1].content}")


def log_output(input):
    if input.content != "":
        logging.info(f"Agent 'researcher' - Thoughts: {input.content}")


chain = (
    RunnablePassthrough(log_input)
    | RunnablePassthrough.assign(examples=add_examples)
    | prompt_researcher
    | wrapper.llm
    | RunnablePassthrough(log_output)
)

researcher = Agent("researcher", chain)