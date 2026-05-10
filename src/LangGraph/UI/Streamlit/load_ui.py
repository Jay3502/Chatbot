import os
import streamlit as st
from src.LangGraph.UI.ui_config import UIConfig

class LoadUI:
    def __init__(self):
        self.ui_config = UIConfig()
        self.user_controls = {}

    def load_ui(self):
        st.set_page_config(page_title=self.ui_config.get_page_title(), layout="wide")
        st.title(self.ui_config.get_page_title())

        # Create a sidebar for navigation
        with st.sidebar:
            llm_options = self.ui_config.get_llm_options()
            usecase_options = self.ui_config.get_usecase_options()

            self.user_controls['selected_llm'] = st.selectbox("Select LLM", llm_options)

            if self.user_controls['selected_llm'] == "Groq":
                model_options = self.ui_config.get_groq_model_options()
                self.user_controls['selected_model'] = st.selectbox("Select Groq Model", model_options)
                self.user_controls['GROQ_API_KEY'] = st.session_state['GROQ_API_KEY'] = st.text_input("GROQ API KEY", type="password")

                if not self.user_controls['GROQ_API_KEY']:
                    st.warning("Please enter your Groq API Key to use the Groq model.")

            # Select Use Case
            self.user_controls['selected_usecase'] = st.selectbox("Select Use Case", usecase_options)

            if self.user_controls["selected_usecase"] == "Web Chatbot":
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state['TAVILY_API_KEY'] = st.text_input("TAVILY API KEY", type="password")
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your TAVILY API Key to use the Web Chatbot.")

        return self.user_controls