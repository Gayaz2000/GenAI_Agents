from utils import ModelLoader
from tools import WeatherInfoTool, PlacesearchTool, CalculatorTool, CurrencyConverterTool
from prompts import SYSTEM_PROMPT
from langgraph.graph import StateGraph,MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from stateflow import State


class Graph_Builder:
    def __init__(self):
        self.tools = [WeatherInfoTool, PlacesearchTool, CalculatorTool, CurrencyConverterTool]
        self.graph = None
        self.system_prompt = SYSTEM_PROMPT
        self.llm_with_tools = ModelLoader().load_llm()

    def agent_function(self, state: MessagesState):
        """Main Agent function"""
        question = state["messages"]
        prompt = [self.system_prompt] + question
        response = self.llm_with_tools.invoke(question)
        return response

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)

        #nodes
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        #edges
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)

        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()