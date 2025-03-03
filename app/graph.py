from langgraph.constants import END
from langgraph.graph import StateGraph
from app.executor.executor import executor
from app.agent import State
from app.responder.responder import responder
from app.planner.planner import planner

builder = StateGraph(State)
builder.add_node(planner.name, planner)
builder.add_node(executor.name, executor)
builder.add_node(responder.name, responder)

builder.add_edge(planner.name, executor.name)
builder.add_edge(executor.name, responder.name)
builder.add_edge(responder.name, END)

# Set Entry point
builder.set_entry_point(planner.name)

graph = builder.compile(debug=False).with_types(input_type=State)
