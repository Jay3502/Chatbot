from dotenv import load_dotenv
load_dotenv()

from src.LangGraph.main import load_app

if __name__ == "__main__":
    load_app()