from app.search import search_chunks
from app.answer import generate_answer

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    question: str
    chunks: list
    answer: str

def retrieve(state: State) -> dict:
    return {"chunks": search_chunks(state["question"])}

def generate(state: State) -> dict:
    return {"answer": generate_answer(state["question"], state["chunks"])}

graph = StateGraph(State)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)

graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)
compiled = graph.compile()

if __name__ == "__main__":
    result = compiled.invoke({"question": "How do I upload a file in FastAPI?"})
    print(result)