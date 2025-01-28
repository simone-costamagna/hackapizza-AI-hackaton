import json

from pydantic import BaseModel, Field
from app.agent import Agent
from app.responder.prompt import prompt_responder
from config import DISH_MAPPING_PATH
from utils.wrapper import LLMWrapper

class Plate(BaseModel):
    name: str = Field(description="Nome del piatto")

class Output(BaseModel):
    plates: list[Plate] = Field(description="Lista di piatti")


with open(DISH_MAPPING_PATH, 'r', encoding='utf-8') as json_file:
    dish_mapping = json.load(json_file)

wrapper = LLMWrapper()
wrapper.set_structured_output(Output)

def map_results(output: Output):
    ids = []
    for plate in output.plates:
        ids.append(dish_mapping[plate.name])

    return ids



chain = (
        prompt_responder
        | wrapper.llm
        | map_results
)

responder = Agent("responder", chain, history=False)

