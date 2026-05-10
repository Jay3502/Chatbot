# LangGraph Streamlit Chatbot

A modular AI chatbot application built using:

* LangGraph
* LangChain
* Streamlit
* Groq LLMs
* Tavily Search API

This project demonstrates how to build both:

1. A basic conversational chatbot
2. A web-enabled chatbot with tool calling support

---

# Features

## Basic Chatbot

* Simple conversational chatbot
* Uses Groq-hosted LLMs
* Built with LangGraph state-based workflows

## Web Chatbot

* Internet-enabled chatbot
* Integrates Tavily Search as a tool
* Demonstrates LangGraph tool routing and conditional edges

## Streamlit UI

* Clean sidebar-based configuration
* Dynamic model selection
* Secure API key input fields

## Modular Architecture

Project is separated into:

* Graphs
* Nodes
* Tools
* Models
* UI
* State management

---

# Project Structure

```text
Chatbot/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   └── LangGraph/
│       ├── Graph/
│       ├── Models/
│       ├── Nodes/
│       ├── State/
│       ├── Tools/
│       └── UI/
│
└── venv/   (should NOT be committed)
```

---

# Tech Stack

| Component       | Technology |
| --------------- | ---------- |
| Frontend        | Streamlit  |
| Workflow Engine | LangGraph  |
| LLM Framework   | LangChain  |
| LLM Provider    | Groq       |
| Web Search Tool | Tavily     |
| Vector Store    | FAISS      |

---

# Installation

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Chatbot
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Required API Keys

This project requires:

| Service        | Purpose         |
| -------------- | --------------- |
| Groq API Key   | LLM access      |
| Tavily API Key | Web search tool |

## Get API Keys

* Groq: [https://console.groq.com/keys](https://console.groq.com/keys)
* Tavily: [https://app.tavily.com/](https://app.tavily.com/)

---

# Running the Application

```bash
streamlit run app.py
```

Then open the local Streamlit URL in your browser.

---

# How It Works

## Graph Builder

The application uses LangGraph to dynamically create workflows.

### Basic Chatbot Flow

```text
START → Chatbot Node → END
```

### Web Chatbot Flow

```text
START → Chatbot → Tools → Chatbot
```

The chatbot can decide when to invoke external tools.

---

# Core Components

## Graph Builder

File:

```text
src/LangGraph/Graph/graph_builder.py
```

Responsible for:

* Building LangGraph workflows
* Adding nodes
* Adding edges
* Tool routing

---

## Nodes

### Basic Chatbot Node

Handles standard LLM responses.

### Chatbot With Tools Node

Handles:

* Tool binding
* Tool invocation
* Returning tool-aware responses

---

## Tools

Current integrated tool:

* Tavily Search

File:

```text
src/LangGraph/Tools/search_tool.py
```

---

## UI

Built with Streamlit.

Features:

* LLM selection
* Model selection
* Use-case selection
* API key input

---

# Current Supported Use Cases

| Use Case      | Description                          |
| ------------- | ------------------------------------ |
| Basic Chatbot | Standard conversational chatbot      |
| Web Chatbot   | Chatbot with internet search support |

---

# Example Workflow

1. Launch the app
2. Select Groq as the LLM
3. Enter your Groq API key
4. Choose a use case
5. (Optional) Add Tavily API key for Web Chatbot
6. Start chatting

---

# Important Notes

## Do NOT Commit Secrets

Add the following to `.gitignore`:

```gitignore
venv/
.env
*.env
__pycache__/
```

---

## Remove venv Before Pushing

The `venv/` directory should not be committed to GitHub.

If already tracked:

```bash
git rm -r --cached venv
```

---

# Future Improvements

Possible enhancements:

* Memory support
* Multi-agent workflows
* RAG pipelines
* Streaming responses
* File upload support
* Conversation history persistence
* Better tool orchestration
* Docker deployment
* Authentication

---

# Dependencies

Main dependencies used:

```text
langchain
langgraph
langchain-openai
langchain-core
langchain-community
langchain-groq
faiss-cpu
streamlit
tavily-python
```

---

# License

This project is intended for learning and experimentation.

You may modify and extend it for personal or educational use.

---

# Author

Built as a modular LangGraph + Streamlit chatbot project for experimenting with agentic AI workflows.
