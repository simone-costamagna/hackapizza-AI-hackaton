import logging
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import tools_condition
from app.agent import State
from app.researcher.researcher import researcher
from app.researcher.tools.tools import tools
from app.researcher.tools.utils import create_tool_node_with_fallback

builder = StateGraph(State)
builder.add_node(researcher.name, researcher)
builder.add_node('tools', create_tool_node_with_fallback(tools))

builder.add_conditional_edges(researcher.name, tools_condition)  # Move to tools after input
builder.add_edge('tools', researcher.name)
builder.add_edge(researcher.name, END)

# Set Entry point
builder.set_entry_point(researcher.name)

graph_researcher = builder.compile(debug=False).with_types(input_type=State)
