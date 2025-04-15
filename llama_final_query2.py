import chromadb
from sentence_transformers import SentenceTransformer
import subprocess
import re

# Load BGE embedding model
print("[~] Loading BGE base model (768D)...")
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chromadb_store")

collections = {
    "Users": client.get_collection("user_embeddings"),
    "Courses": client.get_collection("course_embeddings"),
    "Assignments": client.get_collection("submission_embeddings"),
    "Forum Posts": client.get_collection("forum_post_embeddings")
}

counts = {label: col.count() for label, col in collections.items()}

# Interactive loop
while True:
    query = input("\n🧠> ").strip()
    if query.lower() == "exit":
        print("👋 Goodbye!")
        break

    broad_query = any(keyword in query.lower() for keyword in [
        "list", "show", "students from", "all", "total", "how many", "count"
    ])
    match = re.search(r"\b(\d+)\b", query)
    limit = int(match.group(1)) if match else (100 if broad_query else 3)

    query_embedding = model.encode([query]).tolist()[0]

    context_sections = []

    for label, collection in collections.items():
        try:
            results = collection.query(query_embeddings=[query_embedding], n_results=limit)
            documents = results["documents"][0]
            cleaned = [doc.strip().replace("\n", " ") for doc in documents if doc]
            section = f"\n# {label} (Total Available: {counts[label]}):\n" + "\n".join(cleaned)
            context_sections.append(section)
        except Exception as e:
            context_sections.append(f"# {label}:\n[Error fetching: {e}]")

    context = "\n".join(context_sections)

    # Improved Prompt
    prompt = f"""
You are NIMBLE — Nitte's Intelligent Moodle-Based Learning Engine.
You have access to user, course, assignment, and forum data.

User's Question:
"{query}"

Relevant Data Extracted:
{context}

👉 Important:
- If the question is about totals, counts, or lists, refer directly to the total records or matching context.
- Avoid guessing. If the data isn't sufficient to answer, say: "The exact data isn't available in the current search, but here’s what I found."

Now, write a clear and helpful answer.
"""

    process = subprocess.Popen(["ollama", "run", "llama3"],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)

    output, error = process.communicate(prompt)

    print("\n🤖 NIMBLE says:\n")
    print(output)
    print("\nAsk another question or type 'exit'.")
