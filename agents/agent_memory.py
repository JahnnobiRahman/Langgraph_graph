from typing import List, TypedDict, Union #for handeling the type of the state
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
import os
import platform
import subprocess

from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o", openai_api_key=api_key)


class AgentState(TypedDict):
    messages : List[Union[HumanMessage, AIMessage]]

def process_message(state:AgentState)->AgentState:
    """ """

    response = llm.invoke(state['messages'])

    state['messages'].append(AIMessage(content=response.content))

    print(f"\nAI:{response.content}")
    print("Current State : ", state["messages"])
    return state


graph = StateGraph(AgentState)
graph.add_node("process", process_message)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

# Initialize conversation history
conversation_history = []

while True:
    user_input = input("Enter a message (type 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
        
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]  # Update conversation history with the new state
    
    # Save conversation after each interaction
    try:
        file_path = os.path.join(os.path.dirname(__file__), "chat_history.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Your conversation log:\n\n")
            for message in conversation_history:
                if isinstance(message, HumanMessage):
                    file.write(f"You: {message.content}\n")
                elif isinstance(message, AIMessage):
                    file.write(f"AI: {message.content}\n\n")
            file.write("End of conversation")
        
        print(f"Conversation saved to: {file_path}")
    except Exception as e:
        print("Failed to save conversation:", str(e))

