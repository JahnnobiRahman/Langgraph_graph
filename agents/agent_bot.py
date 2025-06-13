from typing import List, TypedDict
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
import os

from dotenv import load_dotenv

#this code is working but it is not very good at handeling the history of the conversation
#it is not very good at handeling the context of the conversation
#it is not very good at handeling the conversation with the user


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

class AgentState(TypedDict):
    message: List[HumanMessage]

llm = ChatOpenAI(model="gpt-4o", openai_api_key=api_key)
def process_message(state: AgentState) -> AgentState:
    """ """

    response  = llm.invoke(state['message'])
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)

graph.add_node("process", process_message)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()

user_input = input("Enter a message: ")

while(user_input != "exit"):
    agent.invoke({"message": [HumanMessage(content=user_input)]})
    user_input = input("Enter a message: ")



