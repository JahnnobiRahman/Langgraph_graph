# 🧠 LangGraph Practice Project

This project demonstrates a collection of mini graph-based workflows using [LangGraph](https://github.com/langchain-ai/langgraph). Each graph illustrates a different logic pattern — from simple greeting flows to conditional branching and looping with state tracking — perfect for learning stateful program design.

## 📚 Contents

### 🔹 Graph Modules

| File | Description |
|------|-------------|
| `greet_graph.py` | A simple one-node graph that greets the user |
| `math_graph.py` | Performs either sum or multiplication over a list of integers |
| `passion_graph.py` | Chains together name, age, and a passion list into a complete message |
| `branching_math.py` | Performs multi-step conditional math operations (`+`, `-`, `++`, `--`) |
| `loop_random_graph.py` | Continuously appends random numbers until a counter reaches 5 |

---


## Rag_Agent Branch Components


This contains Python scripts for building intelligent AI agents leveraging LangChain, LangGraph, Chroma vector stores, and OpenAI's GPT models. It includes agents designed for document drafting, conversational memory management, external tool execution, and retrieval-augmented generation (RAG).

---

## Components

### 📄 `agent_bot.py`

An AI agent capable of interpreting user requests, executing external tools, and engaging in conversational interactions.

### 🧠 `agent_memory.py`

Enhances conversational abilities by maintaining context and memory across interactions, providing coherent and context-aware responses.

### 📝 `drafter.py`

Specialized agent for creating, editing, and managing documents. Supports content updates, draft persistence, and interactive collaboration with users.

### 🔍 `rag_agent.py`

Utilizes Retrieval-Augmented Generation (RAG) techniques to enrich AI responses by retrieving relevant information from external documents using Chroma vector stores and embeddings.

### 💌 `Love_Letter_to_Joy.txt`

A personal, heartfelt letter demonstrating the type of content managed or created by the drafting agent.

### 💬 `chat_history.txt`

Sample conversation log illustrating basic conversational flow and AI interactions.

---

## Key Technologies Used

* **LangChain & LangGraph:** Frameworks for creating sophisticated conversational AI agents.
* **Chroma Vector Store:** Stores and retrieves embeddings efficiently for semantic search and retrieval.
* **OpenAI GPT-4o:** Advanced language understanding and generation model.
* **Python:** Primary programming language used throughout.

---

## Functional Highlights

* **Conversational AI:** Maintains coherent conversations with context awareness.
* **Tool Invocation:** Executes external tools based on user interactions.
* **Memory Management:** Preserves conversational history for nuanced interactions.
* **Document Drafting:** Enables collaborative creation, editing, and document management.
* **RAG Integration:** Enhances accuracy and relevance of AI responses through external document retrieval.

---

## Usage

Run individual Python scripts as needed. Ensure required dependencies (`langchain`, `langgraph`, `chromadb`, `openai`) are installed.

Example:

```bash
python drafter.py
```

---

## Setup

Install dependencies:

```bash
pip install langchain langgraph chromadb openai python-dotenv
```

Set required environment variables (e.g., OpenAI API key):

```bash
export OPENAI_API_KEY='your_openai_api_key_here'
```

---

## Folder Structure

```plaintext
project/
├── agent_bot.py
├── agent_memory.py
├── drafter.py
├── rag_agent.py
├── Love_Letter_to_Joy.txt
├── chat
```
