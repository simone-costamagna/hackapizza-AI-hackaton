from langgraph.constants import END
from langgraph.graph import StateGraph
from app.agent import State
from app.researcher.graph_researcher import graph_researcher
from app.responder.responder import responder
from app.planner.planner import planner

builder = StateGraph(State)
builder.add_node("planner", planner)
builder.add_node("graph_researcher", graph_researcher)
builder.add_node(responder.name, responder)

builder.add_edge(planner.name, "graph_researcher")
builder.add_edge("graph_researcher", responder.name)
builder.add_edge(responder.name, END)

# Set Entry point
builder.set_entry_point(planner.name)

graph = builder.compile(debug=False).with_types(input_type=State)
