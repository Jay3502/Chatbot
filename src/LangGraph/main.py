import streamlit as st
from src.LangGraph.UI.Streamlit.load_ui import LoadUI
from src.LangGraph.Models.groqllm import GroqLLM
from src.LangGraph.Graph.graph_builder import GraphBuilder
from src.LangGraph.UI.Streamlit.display import Display

def _keys_ready(user_input):
    """Return (ready, warning_message) based on which keys are missing."""
    groq_key = user_input.get("GROQ_API_KEY", "").strip()
    usecase = user_input.get("selected_usecase", "")

    if not groq_key:
        return False, None  # warning already shown by load_ui

    if usecase == "Web Chatbot":
        tavily_key = user_input.get("TAVILY_API_KEY", "").strip()
        if not tavily_key:
            return False, None  # warning already shown by load_ui

    return True, None


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
    usecase = user_input.get('selected_usecase')
    if not usecase:
        st.error("Error: No use case selected.")
        return

    # Always render chat input so the UI is fully visible
    # even before the API keys are entered.
    user_message = st.chat_input("Enter your message:")

    # Show sidebar/chat history even when keys are missing
    if not _keys_ready(user_input)[0]:
        Display(usecase, graph=None, user_message=None).display_results()
        return

    # ----------------------------------------------------------
    # Build and cache the graph in session state so it survives
    # Streamlit reruns. Include key fingerprints in the cache key
    # so the graph is rebuilt when keys change.
    # ----------------------------------------------------------
    groq_key = user_input.get("GROQ_API_KEY", "").strip()
    tavily_key = user_input.get("TAVILY_API_KEY", "").strip()
    graph_cache_key = f"graph_{usecase}_{user_input.get('selected_model', '')}_{groq_key[:6]}_{tavily_key[:6]}"

    if graph_cache_key not in st.session_state:
        try:
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return

        if not model:
            Display(usecase, graph=None, user_message=None).display_results()
            return

        try:
            graph = GraphBuilder(model).setup_graph(usecase)
            st.session_state[graph_cache_key] = graph
        except Exception as e:
            st.error(f"Error: Failed to setup graph for use case '{usecase}': {str(e)}")
            return
    else:
        graph = st.session_state[graph_cache_key]

    Display(usecase, graph, user_message).display_results()