from configparser import ConfigParser

class UIConfig:
    def __init__(self, config_file = "./src/LangGraph/UI/ui_config.ini"):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")

    def get_llm_options(self):
        return [x.strip() for x in self.config["DEFAULT"].get("LLM_OPTIONS").split(',')]

    def get_usecase_options(self):
        return [x.strip() for x in self.config["DEFAULT"].get("USECASE_OPTIONS").split(',')]

    def get_groq_model_options(self):
        return [x.strip() for x in self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(',')]