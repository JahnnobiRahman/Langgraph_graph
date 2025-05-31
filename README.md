🧠 LangGraph Practice Notebook

This project is a collection of mini-graph-based logic flows built using LangGraph. It includes hands-on examples of 

greeting workflows, math operations, loops, branching with conditions, and node chaining—all inside Python.

📂 Contents

✅ Graph Examples Included:

Graph

Description

Greeting

Simple graph to greet a user

Math Operation

Graph that performs addition or multiplication

Passion Printer

Graph that prints name, age, and list of passions

Branching Calculator

Nested conditional graph for multiple arithmetic branches

Random Loop Generator

Repeats a node until a counter reaches 5

📁 Files

Exercise_Graph5.ipynb: The main Jupyter notebook containing all graph code blocks

Images: Generated automatically using draw_mermaid_png() from langgraph

DOTENV support is included for managing API keys via .env

📌 Requirements

Install all dependencies using pip:

pip install langgraph langchain langchain-core langchain-community langchain-openai ollama openai ipython graphviz notebook

▶️ How to Use

1. Clone this repository:

git clone https://github.com/your-username/langgraph-practice.git
cd langgraph-practice

2. Activate Jupyter Notebook:

jupyter notebook Exercise_Graph5.ipynb

3. Run Graphs

Each graph is self-contained in a notebook cell. You can:

Compile the graph using graph.compile()

Print or Visualize it:

app.get_graph().print_ascii()
display(Image(app.get_graph().draw_mermaid_png()))

Invoke the graph:

app.invoke({...})

🔄 Examples

Greeting Graph

__start__ → greeter → __end__

Looping Random Graph

__start__ → greeting → random
     ↑        ↓
   loop ← random → exit → __end__

Branching Arithmetic Graph

__start__ → router1 → (add | sub) → router2 → (add1 | sub1) → __end__

🔐 API Keys

Add your OpenAI key in a .env file like so:

OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXX

Or set it in Python via:

import os
os.environ["OPENAI_API_KEY"] = "sk-..."

📌 Notes

This project is experimental and designed for learning LangGraph.

Mermaid graphs are rendered using IPython's display(Image(...)).

Error handling and flow visualization are built-in.

🙌 Acknowledgements

Made with ❤️ using:

LangGraph

LangChain

Graphviz

✍️ Author

Jahnnobi,

