import logging
from typing import List
from langchain_core.runnables import Runnable
from typing_extensions import TypedDict

class State(TypedDict):
    main_question: str
    questions: List[str] = []
    responses: List[str] = []
    final_response: List[int] = []

class Agent:
    def __init__(self, name: str, runnable: Runnable):
        self.name = name
        self.runnable = runnable

    def __call__(self, state: State):
        logging.info(f"Agent '{self.name}' has started execution.")

        response = self.runnable.invoke(state)

        logging.info(f"Agent '{self.name}' has finished execution.")

        # Return the final state after processing the runnable
        return response