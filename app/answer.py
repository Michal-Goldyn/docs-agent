from app.search import search_chunks
from app.config import settings
from anthropic import Anthropic

client = Anthropic()

def doc_url(source: str = "https://fastapi.tiangolo.com/tutorial/"):
    return settings.docs_base_url + source.removesuffix(".md")

def answer(question: str) -> str:

    reply = search_chunks(question)

    if reply and (reply[0]["similarity"] >= settings.similarity_threshold):

        context = ""
        for i, chunk in enumerate(reply):
            context += f"[{i+1}] source: {chunk['source']} | url: {doc_url(chunk['source'])} | section: {chunk['section']}\n"
            context += chunk['content'] + "\n\n"
        
        message = client.messages.create(
            model = "claude-haiku-4-5",
            max_tokens=1024,
            system = f"""You are a documentation assistant. Answer using ONLY the context above.

                        Rules:
                        - If the context does not contain the answer, reply exactly: "I didn't find an answer in the documentation."
                        - Never use knowledge outside the context. Never invent code or APIs.
                        - Be precise and concise.
                        - After each claim, put the source url in parentheses on the same line, e.g. (https://fastapi.tiangolo.com/tutorial/request-files/). Do not add a list of sources at the end.
                        
                        Context: 
                        <context>
                            {context}
                        </context>
                        """,
            messages=[
                {
                    "role": "user",
                    "content": question,
                }
            ]
        )
        return message.content[0].text

    else:
        return "I didn't find proper data in the database"


if __name__ == "__main__":
    #print(answer("How do I upload a file in FastAPI?"))
    print(answer("How do I train a neural network in PyTorch?"))