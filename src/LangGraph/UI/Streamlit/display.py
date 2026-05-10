import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json, uuid

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

        if "chats" not in st.session_state:

            first_thread = str(uuid.uuid4())

            st.session_state.chats = {
                "Chat 1": first_thread
            }

        if "selected_chat" not in st.session_state:
            st.session_state.selected_chat = "Chat 1"

        # =========================
        # Sidebar
        # =========================

        st.sidebar.title("Chats")

        # Create New Chat
        if st.sidebar.button("New Chat"):

            new_chat_name = (
                f"Chat {len(st.session_state.chats)+1}"
            )

            new_thread_id = str(uuid.uuid4())

            st.session_state.chats[
                new_chat_name
            ] = new_thread_id

            # update selected chat
            st.session_state.selected_chat = (
                new_chat_name
            )

        # Chat list
        chat_list = list(
            st.session_state.chats.keys()
        )

        # determine selected index
        selected_index = chat_list.index(
            st.session_state.selected_chat
        )

        # IMPORTANT:
        # use unique key + selected index
        selected_chat = st.sidebar.radio(
            "Select Chat",
            options=chat_list,
            index=selected_index,
            key=f"chat_radio_{selected_index}"
        )

        # persist selection
        st.session_state.selected_chat = (
            selected_chat
        )

        # =========================
        # Config
        # =========================

        thread_id = st.session_state.chats[
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

        state = graph.get_state(config)

        old_messages = []

        if state.values:

            old_messages = state.values.get(
                "messages",
                []
            )

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