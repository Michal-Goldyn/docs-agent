from app.search import search_chunks
from app.answer import generate_answer
from app.config import settings

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    """State passed between graph nodes: the question, retrieved chunks, final answer."""
    question: str
    chunks: list
    answer: str

def retrieve(state: State) -> dict:
    """Search the docs and keep only chunks above the similarity threshold."""
    chunks = search_chunks(state["question"])
    good_chunks = [c for c in chunks if c["similarity"] >= settings.similarity_threshold]
    return {"chunks": good_chunks}

def generate(state: State) -> dict:
    """Generate an answer from the retrieved chunks."""
    return {"answer": generate_answer(state["question"], state["chunks"])}

def route_after_retrieve(state: State) -> str:
    """Route to generation if any chunk passed the threshold, otherwise to no_answer."""
    return "generate" if state["chunks"] else "no_answer"

def no_answer(state: State) -> dict:
    """Return a fixed message when retrieval found nothing relevant."""
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


rag_graph = graph.compile()

if __name__ == "__main__":
    #print(rag_graph.invoke({"question": "How do I upload a file in FastAPI?"})["answer"])
    #print("---")
    #print(rag_graph.invoke({"question": "How do I train a neural network in PyTorch?"})["answer"])
    print(rag_graph.get_graph().draw_mermaid())