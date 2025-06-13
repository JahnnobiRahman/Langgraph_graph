from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from operator import add as add_messages
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.tools import tool

load_dotenv()

llm=ChatOpenAI(model = "gpt-4o", temperature=0)

embeddings = OpenAIEmbeddings(
    model = "text-embedding-3-small", 
)

pdf_path = "/Users/jahnnobirahman/Desktop/python/allcode/projects/Langgraph_graph/agents/david-allen-getting-things-done-the-art-of-stress-free-productivity-penguin-358-pages_compress.pdf"

# Safety measure I have put for debugging purposes :)
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path)


# Checks if the PDF is there
try:
    pages = pdf_loader.load()
    print(f"PDF has been loaded and has {len(pages)} pages")
except Exception as e:
    print(f"Error loading PDF: {e}")
    raise


text_splitter = RecursiveCharacterTextSplitter(

    chunk_size = 1000,
    chunk_overlap = 300
)

pages_split = text_splitter.split_documents(pages)

persist_directory = r"/Users/jahnnobirahman/Desktop/python/allcode/projects/Langgraph_graph/agents "

collection_name = "daily_work"

# If our collection does not exist in the directory, we create using the os command
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)


#now we create vector database using Chroma


try: 

    vectorstore = Chroma.from_documents(

        documents = pages_split,
        embedding=  embeddings,
        collection_name =  collection_name,
        persist_directory = persist_directory

    )

    print(f"Created Chroma-DB vector store")

except Exception as e : 

    print(f"error setting of Chroma DB : {str(e)}")


    raise


#now we use retriver, which retrieved the most similar chunks 


retriever = vectorstore.as_retriever(

    search_type="mmr",
        search_kwargs={'k': 6, 'lambda_mult': 0.25}
)


#now we create a tool to that will show the retrived informations


@tool
def retriever_tool(query: str) -> str:
    """Retrieve relevant information from the document."""
    docs = retriever.get_relevant_documents(query)  # Fixed: using get_relevant_documents instead of query
    if not docs:
        return "I found no relevant information to process your daily routine."
    
    results = []
    for i, doc in enumerate(docs):
        results.append(f"Document {i+1}:\n{doc.page_content}")
                       
    return "\n\n".join(results)



tools = [retriever_tool]

llm = llm.bind_tools(tools)


class AgentState(TypedDict) :
    messages : Annotated[Sequence[BaseMessage], add_messages]


def should_continue(state:AgentState)->AgentState:

    """ """

    result = state["messages"][-1]
    return hasattr (result, "tool_calls")  and len(result.tool_calls)>0


system_prompt = """

You are a highly efficient, intuitive Daily Task Manager designed specifically to optimize my personal and professional productivity. You will help me manage and track tasks related to:

Professional Tasks: Project deadlines, meetings, work assignments, skill development activities.

Health & Fitness: Gym sessions, diet tracking, hydration reminders, and rest periods.

Hobbies & Interests: Art projects, reading lists, language practice, gardening tasks, coding practice.

Mental Well-being: Meditation sessions, journaling, mindfulness exercises, and relaxation breaks.

Social Activities: Family time, social events, catch-ups with friends, and community activities.

For each task, clearly identify:

Task Name

Category (Professional, Health & Fitness, Hobbies & Interests, Mental Well-being, Social Activities)

Priority Level (High, Medium, Low)

Duration or Scheduled Time

Notes or Special Instructions

Your goal is to proactively prompt me daily, keeping track of incomplete tasks, rescheduling as necessary, and reminding me about upcoming important dates or recurring activities. Provide insightful weekly summaries highlighting my productivity patterns, accomplishments, and areas for improvement.




"""


tools_dict = {our_tool.name : our_tool for our_tool in tools } 

def call_llm(state: AgentState) -> AgentState:
    """Process messages through the LLM."""
    messages = list(state["messages"])
    messages = [SystemMessage(content=system_prompt)] + messages  # Fixed: removed quotes around messages
    message = llm.invoke(messages)
    return {"messages": [message]}


def take_action(state: AgentState) -> AgentState:
    """Execute tool calls."""
    tool_calls = state["messages"][-1].tool_calls  # Fixed: using messages instead of message
    results = []

    for tool_call in tool_calls:  # Fixed: renamed tool to tool_call
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        print(f"\nCalling tool {tool_name} with args: {tool_args}")

        if tool_name not in tools_dict:
            print(f"Tool name: {tool_name} does not exist")
            result = "Incorrect, try again"
        else:
            tool_function = tools_dict[tool_name]
            query = tool_args.get("query", " ")
            result = tool_function.invoke(query)
            print(f"✅ Tool '{tool_name}' executed successfully. Result length: {len(str(result))}")
            
        results.append(ToolMessage(tool_call_id=tool_call['id'], name=tool_call['name'], content=str(result)))  # Fixed: using tool_call instead of t

    print("Tools Execution Complete. Back to the model!")
    return {'messages': results}


graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)

graph.add_conditional_edges(
    "llm",
    should_continue,
    {True: "retriever_agent", False: END}
)
graph.add_edge("retriever_agent", "llm")
graph.set_entry_point("llm")

rag_agent = graph.compile()


def running_agent():
    print("\n=== RAG AGENT===")
    
    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        messages = [HumanMessage(content=user_input)] # converts back to a HumanMessage type

        result = rag_agent.invoke({"messages": messages})
        
        print("\n=== ANSWER ===")
        print(result['messages'][-1].content)


running_agent()