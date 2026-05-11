import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json, uuid
from src.LangGraph.Memory.sqlite_memory import load_chats, save_chat

class Display:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_results(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        # =========================
        # Session Initialization
        # =========================

        # Use per-usecase keys so each usecase has its own
        # independent chat list and selected chat in session state.
        chats_key = f"chats_{usecase}"
        selected_key = f"selected_chat_{usecase}"

        if chats_key not in st.session_state:
            # Load persisted chats for this usecase from DB
            persisted = load_chats(usecase)
            if persisted:
                st.session_state[chats_key] = persisted
            else:
                first_thread = str(uuid.uuid4())
                st.session_state[chats_key] = {"Chat 1": first_thread}
                save_chat("Chat 1", first_thread, usecase)

        if selected_key not in st.session_state:
            st.session_state[selected_key] = next(
                iter(st.session_state[chats_key])
            )

        # =========================
        # Sidebar
        # =========================

        st.sidebar.title("Chats")

        # Create New Chat
        if st.sidebar.button("New Chat"):

            new_chat_name = (
                f"Chat {len(st.session_state[chats_key])+1}"
            )

            new_thread_id = str(uuid.uuid4())

            st.session_state[chats_key][
                new_chat_name
            ] = new_thread_id

            # Persist to DB under this usecase
            save_chat(new_chat_name, new_thread_id, usecase)

            # Update both the selection state and the radio widget
            # state directly - otherwise Streamlit ignores the index
            # parameter on rerun and the radio stays on the old chat.
            st.session_state[selected_key] = new_chat_name
            st.session_state[f"chat_radio_{usecase}"] = new_chat_name

        # Chat list
        chat_list = list(
            st.session_state[chats_key].keys()
        )

        # Value is managed entirely via session state (no index=) to avoid
        # Streamlit's 'default value + session state' conflict warning.
        # Initialise the radio's own key from selected_key if not yet set.
        radio_key = f"chat_radio_{usecase}"
        if radio_key not in st.session_state:
            st.session_state[radio_key] = st.session_state[selected_key]

        selected_chat = st.sidebar.radio(
            "Select Chat",
            options=chat_list,
            key=radio_key
        )

        # persist selection
        st.session_state[selected_key] = selected_chat

        # =========================
        # Config
        # =========================

        thread_id = st.session_state[chats_key][
            selected_chat
        ]

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        # =========================
        # Load Old Messages
        # =========================

        old_messages = []

        if graph is not None:
            state = graph.get_state(config)
            if state.values:
                old_messages = state.values.get("messages", [])

        # =========================
        # Display Old Messages
        # =========================

        for message in old_messages:

            if isinstance(
                message,
                HumanMessage
            ):

                with st.chat_message("user"):
                    st.write(message.content)

            elif isinstance(
                message,
                AIMessage
            ):

                if message.content:

                    with st.chat_message(
                        "assistant"
                    ):

                        st.write(message.content)

            elif isinstance(
                message,
                ToolMessage
            ):

                with st.chat_message(
                    "assistant"
                ):

                    st.write(message.content)

        # =========================
        # Basic Chatbot
        # =========================

        if (
            usecase == "Basic Chatbot"
            and user_message
            and graph is not None
        ):

            for event in graph.stream(
                {
                    "messages": [
                        HumanMessage(
                            content=user_message
                        )
                    ]
                },
                config=config
            ):

                for value in event.values():

                    assistant_message = (
                        value["messages"]
                    )

                    # User Message
                    with st.chat_message("user"):
                        st.write(user_message)

                    # Assistant Message
                    if isinstance(
                        assistant_message,
                        AIMessage
                    ):

                        with st.chat_message(
                            "assistant"
                        ):

                            st.write(
                                assistant_message.content
                            )

        # =========================
        # Web Chatbot
        # =========================

        elif (
            usecase == "Web Chatbot"
            and user_message
            and graph is not None
        ):

            initial_state = {
                "messages": [
                    HumanMessage(
                        content=user_message
                    )
                ]
            }

            res = graph.invoke(
                initial_state,
                config=config
            )

            for message in res["messages"]:

                if isinstance(
                    message,
                    HumanMessage
                ):

                    with st.chat_message(
                        "user"
                    ):

                        st.write(
                            message.content
                        )

                elif isinstance(message, ToolMessage):
                    with st.chat_message("ai"):
                        st.write("Tool Call Start")
                        st.write(message.content)
                        st.write("Tool Call End")
                elif (isinstance(message, AIMessage) and message.content):
                    with st.chat_message("assistant"):
                        st.write(message.content)