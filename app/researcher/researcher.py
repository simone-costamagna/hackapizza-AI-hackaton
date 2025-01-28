import logging
from app.agent import Agent
from app.researcher.prompts import prompt_researcher
from utils.wrapper import LLMWrapper
from app.researcher.tools.tools import retrieve_functional_context, retrieve_technical_context

wrapper = LLMWrapper()
wrapper.bind_tools([retrieve_functional_context, retrieve_technical_context])


def log_researcher(status):
    logging.info("Researcher started execution")


chain = (
    prompt_researcher
    | wrapper.llm
)

researcher = Agent("researcher", chain)