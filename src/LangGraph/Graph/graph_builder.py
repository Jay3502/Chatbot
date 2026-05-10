from langgraph.graph import START, StateGraph, END
from src.LangGraph.State.state import State
from src.LangGraph.Nodes.basic_chatbot_node import BasicChatbotNode
from src.LangGraph.Tools.search_tool import get_tools, create_tool_nodes
from langgraph.prebuilt import ToolNode, tools_condition
from src.LangGraph.Nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.LangGraph.Memory.sqlite_memory import get_memory

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tools_build_graph(self):
        tools = get_tools()
        tool_nodes = create_tool_nodes(tools)

        llm = self.llm
        obj_chatbot_node = ChatbotWithToolNode(self.llm)
        chatbot_node = obj_chatbot_node.create_chatbot(tools)

        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_nodes)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")

    def setup_graph(self, usecase):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Web Chatbot":
            self.chatbot_with_tools_build_graph()
        else:
            raise ValueError(f"Unsupported use case: {usecase}")

        memory = get_memory()
        return self.graph_builder.compile(checkpointer=memory)