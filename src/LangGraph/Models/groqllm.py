import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input.get("GROQ_API_KEY", "").strip()
            selected_groq_model = self.user_controls_input.get("selected_model", "")

            if not groq_api_key:
                groq_api_key = os.getenv("GROQ_API_KEY", "")

            if not groq_api_key:
                st.warning("Please enter your Groq API Key.")
                return None

            llm=ChatGroq(api_key=groq_api_key, model=selected_groq_model)
            
        except Exception as e:
            raise ValueError(f"Error occurred with Exception: {e}")
        
        return llm