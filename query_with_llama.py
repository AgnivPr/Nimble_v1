# query_with_llama.py

import chromadb
from sentence_transformers import SentenceTransformer
import subprocess
import re

# Load embedding model
print("[~] Loading BGE base model (768D)...")
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chromadb_store")

# Access all collections
collections = {
    "Users": client.get_collection("user_embeddings"),
    "Courses": client.get_collection("course_embeddings"),
    "Assignments": client.get_collection("submission_embeddings"),
    "Forum Posts": client.get_collection("forum_post_embeddings")
}

# 🧠 Count actual records to use in summary prompts
counts = {label: col.count() for label, col in collections.items()}

# 🧠 Start Q&A loop
while True:
    query = input("\n🧠> ").strip()
    if query.lower() == "exit":
        print("👋 Goodbye!")
        break

    # Determine how many results to retrieve
    broad_query = any(keyword in query.lower() for keyword in [
        "list", "show all", "get all", "students from", "give me", "total", "count", "how many"
    ])
    match = re.search(r"\b(\d+)\b", query)
    limit = int(match.group(1)) if match else (100 if broad_query else 3)

    # Get query embedding
    query_embedding = model.encode([query]).tolist()[0]

    # Gather relevant docs from each collection
    context_sections = []

    for label, collection in collections.items():
        try:
            results = collection.query(query_embeddings=[query_embedding], n_results=limit)
            documents = results["documents"][0]
            cleaned_docs = [doc.strip().replace("\n", " ") for doc in documents if doc]
            section = f"\n# {label} (Total Records: {counts[label]}):\n" + "\n".join(cleaned_docs)
            context_sections.append(section)
        except Exception as e:
            context_sections.append(f"# {label}:\n[Error fetching data: {e}]")

    # Combine context
    context = "\n".join(context_sections)

    # LLaMA Prompt
    prompt = f"""
You are a helpful assistant analyzing Moodle data.

User Query: "{query}"

Here is the retrieved context from the Moodle system:
{context}

Please answer the user query above in a clear, friendly, human-like tone. If the user asks for totals or lists, make sure to reference all available records. If context is missing, politely say so.
"""

    # Run LLaMA
    process = subprocess.Popen(["ollama", "run", "llama3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate(prompt)

    print("\n🤖 LLaMA says:\n")
    print(output)
    print("\nAsk another question or type 'exit'.")

