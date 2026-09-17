from app.search import search_chunks
from app.answer import generate_answer
from app.config import settings

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

def route_after_retrieve(state: State) -> str:
    if state["chunks"] and (state["chunks"][0]["similarity"] >= settings.similarity_threshold):
        return "generate"
    else: 
        return "no_answer"

def no_answer(state: State) -> dict:
    return {"answer": "I didn't find an answer in the documentation."}

graph = StateGraph(State)
graph.add_node("retrieve", retrieve)
graph.add_node("generate", generate)
graph.add_node("no_answer", no_answer)

graph.add_edge(START, "retrieve")
graph.add_conditional_edges("retrieve", route_after_retrieve, {
    "generate": "generate",
    "no_answer": "no_answer"
})
graph.add_edge("no_answer", END)
graph.add_edge("generate", END)


compiled = graph.compile()

if __name__ == "__main__":
    print(compiled.invoke({"question": "How do I upload a file in FastAPI?"})["answer"])
    print("---")
    print(compiled.invoke({"question": "How do I train a neural network in PyTorch?"})["answer"])