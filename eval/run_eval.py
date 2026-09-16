import json
from pathlib import Path
from app.search import search_chunks

def run():
    questions = json.loads(Path("eval/questions.json").read_text(encoding="utf-8"))

    counter = 0

    for item in questions:
        results = search_chunks(item["q"])
        sources = [result["source"] for result in results]

        position = None
        for i, src in enumerate(sources):
            if src in item["expected"]:
                position = i + 1
                break

        if position:
            print(f"OK [{position}]: {item['q']}")
            counter += 1
        else:
            print(f"MISS: {item['q']}")

    print("\n\n----- SUMMARY -----")
    print("Hits: ", counter)
    print("Number of questions: ", len(questions))

if __name__ == "__main__":
    run()
    #for r in search_chunks("how do I stop the browser from blocking my API calls?"):
    #    print(r["source"], "|", r["section"], "|", round(r["similarity"], 3))
