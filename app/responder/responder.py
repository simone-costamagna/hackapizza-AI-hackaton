import json
import logging

from Levenshtein import distance
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
dish_mapping = {key.lower(): value for key, value in dish_mapping.items()}

wrapper = LLMWrapper()
wrapper.set_structured_output(Output)

def map_results(output: Output):
    ids = []
    for plate in output.plates:
        try:
            ids.append(dish_mapping[plate.name.lower()])
        except Exception as ex:
            best_match = None
            min_distance = 0

            for key in dish_mapping.keys():
                dist = distance(plate.name.lower(), key)
                if best_match is None or dist < min_distance:
                    min_distance = dist
                    best_match = key

            logging.info(f"Key {plate.name.lower()} not found. Found {best_match} with similarity")
            ids.append(dish_mapping[best_match])

    return ids



chain = (
        prompt_responder
        | wrapper.llm
        | map_results
)

responder = Agent("responder", chain, history=False)

