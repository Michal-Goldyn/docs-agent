from openai import OpenAI

client = OpenAI()

def embed(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text, model="text-embedding-3-small"
    )
    return response.data[0].embedding

def embed_many(text: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        input=text, model="text-embedding-3-small"
    )
    return [item.embedding for item in response.data]

if __name__ == "__main__":
    vs = embed_many(["FastAPI file upload", "chocolate cake"])
    print(len(vs), len(vs[0]))