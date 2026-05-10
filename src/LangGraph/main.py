import streamlit as st
from src.LangGraph.UI.Streamlit.load_ui import LoadUI
from src.LangGraph.Models.groqllm import GroqLLM
from src.LangGraph.Graph.graph_builder import GraphBuilder
from src.LangGraph.UI.Streamlit.display import Display

def load_app():
    """
    Load the Streamlit application UI and return user controls. 
    Initializes the LoadUI class and calls the load_ui method to set up the interface.
    """
    ui = LoadUI()
    user_input = ui.load_ui()

    if not user_input:
        st.error("Error: Failed to load user controls.")
        return
    
    user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: Failed to initialize the language model.")
                return
            
            usecase = user_input.get('selected_usecase')
            if not usecase:
                st.error("Error: No use case selected.")
                return
            
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                Display(usecase, graph, user_message).display_results()
            except Exception as e:
                st.error(f"Error: Failed to setup graph for use case '{usecase}': {str(e)}")
                return
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return