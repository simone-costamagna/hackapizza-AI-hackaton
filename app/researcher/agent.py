import logging
from typing import Annotated
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    schema: str
    output: list[int]


class Agent:
    def __init__(self, name: str, runnable: Runnable, history=True):
        self.name = name
        # Initialize with the runnable that defines the process for interacting with the tool
        self.runnable = runnable
        self.history = history

    def __call__(self, state: State):
        logging.info(f"Agent '{self.name}' has started execution.")

        while True:
            # Invoke the runnable with the current state (messages and context)
            if not self.history:
                state['messages'] = [state['messages'][-1]]

            result = self.runnable.invoke(state, RunnableConfig(recursion_limit=60))

            # If the agent used tools
            if hasattr(result, "tool_calls") and len(result.tool_calls) > 0:
                # If the tool fails to return valid output, re-prompt the user to clarify or retry
                if not result.tool_calls and (
                        not result.content
                        or isinstance(result.content, list)
                        and not result.content[0].get("text")
                ):
                    # Add a message to request a valid response
                    messages = state["messages"] + [("user", "Respond with a real output.")]
                    state = {**state, "messages": messages}
                else:
                    # Break the loop when valid output is obtained
                    response = {"messages": result}
                    break
            else:
                if not isinstance(result, AIMessage):
                    response = {"output": result}
                else:
                    response = {"messages": result}
                break

        logging.info(f"Agent '{self.name}' has finished execution.")

        # Return the final state after processing the runnable
        return response