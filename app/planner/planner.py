import logging
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from app.agent import Agent
from app.planner.prompt import prompt_planner
from utils.models import GPT_03_MINI
from utils.wrapper import LLMWrapper


def extract_questions(output):
    return output.questions

def log(status):
    logging.info(f"Agent 'planner' - Sotto-domande: {status['questions']}")


class Output(BaseModel):
    questions: list[str] = Field(description="Lista di sotto-domande")

wrapper = LLMWrapper(model_id=GPT_03_MINI)
wrapper.set_structured_output(Output)

chain = (
    RunnablePassthrough.assign(questions=prompt_planner | wrapper.llm | extract_questions)
    | RunnablePassthrough(log)
)

planner = Agent("planner", chain)

