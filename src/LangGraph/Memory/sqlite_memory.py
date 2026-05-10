import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver


def get_memory():

    conn = sqlite3.connect(
        "chatbot_memory.db",
        check_same_thread=False
    )

    memory = SqliteSaver(conn)

    return memory