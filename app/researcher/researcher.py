import logging

from langchain_core.runnables import RunnablePassthrough

from app.agent import Agent
from app.researcher.prompts import prompt_researcher
from utils.wrapper import LLMWrapper
from app.researcher.tools.tools import retrieve_functional_context, retrieve_technical_context

wrapper = LLMWrapper()
wrapper.bind_tools([retrieve_functional_context, retrieve_technical_context])


def log_output(input):
    if input.content != "":
        logging.info(f"Researcher answer: {input.content}")


chain = (
    prompt_researcher
    | wrapper.llm
    | RunnablePassthrough(log_output)
)

researcher = Agent("researcher", chain)