from typing import Annotated, Sequence, TypedDict #for handeling the type of the state
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END, START
import os


from dotenv import load_dotenv


load_dotenv()

document_content = " "


class AgentState(TypedDict) :
    messages:Annotated[Sequence[BaseMessage], add_messages]


@tool
def update(content:str)->str :
    """ updates the documens content"""
    global document_content
    document_content = content 
    return f"document has been updated successfully! The current content is :\n{document_content}"

@tool

def save(filename:str)->str :
    """
    Save the documents in a text file

    Args :

        filename : name for the text file
    """

    if not filename.endswith('.txt'):
        filename=f"{filename}.txt"


    try:
        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(document_content)
        print(f"Conversation saved to: {filename}")
        return f"Document has been saved successfully to '{filename}'."


    except Exception as e:
        return f"Error saving document: {str(e)}"



tools = [update, save]

model = ChatOpenAI(model="gpt-4o").bind_tools(tools)

def our_agent (state : AgentState) ->AgentState:
    system_prompt = SystemMessage(content=f"""

    You are an AI assistant working inside an AI Agentic System designed to help a company draft documents faster and more efficiently.

    The company is currently wasting too much time on manual drafting of documents and emails. Your goal is to collaborate with a human user to speed up this process.

    Your responsibilities:

    Prompt the human user to describe what they want in a document or email.

    Based on their input, generate a clear and concise draft.

    After each draft, ask the human whether they want to revise, continue, or finalize.

    Be open to continuous feedback, adapting the draft until the human is satisfied.

    End the drafting process only when the human says they are happy with the draft.

    Guidelines:

    Always keep a collaborative tone.

    Don't assume finality — always check in.

    Focus on clarity and speed, but allow flexibility in tone/style based on user preferences.

    Begin the session by asking:
    “Hi! I’m your AI writing assistant. What would you like to draft today?”

    the current document content is : {document_content}

""")
    if not state["messages"]:
        user_input = "I'm ready to help you update a document. What would you like to create?"
        user_message = HumanMessage(content=user_input)

    else:
        user_input = input("\nWhat would you like to do with the document? ")
        print(f"\n👤 USER: {user_input}")
        user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt]+list(state["messages"]) + [user_message]

    response = model.invoke(all_messages)


    print(f"\nAI:{response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"🔧 USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state["messages"]) + [user_message, response]}


def should_continue (state:AgentState)->str :
    """ """
    messages = state["messages"]
    if not messages : 
        return "continue" 
    
    for message in reversed(messages) :
        if(isinstance(message, ToolMessage) and
            "saved" in message.content.lower() and
            "document" in message.content.lower()) :
            return "end"
        
    return "continue"


def print_messages(messages):
    """Function I made to print the messages in a more readable format"""
    if not messages:
        return
    
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n🛠️ TOOL RESULT: {message.content}")


graph = StateGraph(AgentState)

graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")

graph.add_edge("agent", "tools")

graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue": "agent",
        "end": END
    }
)
app = graph.compile()


def run_document_agent():
    print("\n ===== DRAFTER =====")
    
    state = {"messages": []}
    
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== DRAFTER FINISHED =====")

if __name__ == "__main__":
    run_document_agent()
