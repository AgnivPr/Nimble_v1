# llama_final_query.py

import chromadb
from sentence_transformers import SentenceTransformer
import subprocess
import re

# Load embedding model
print("[~] Loading BGE base model (768D)...")
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chromadb_store")

# All collections
collections = {
    "Users": client.get_collection("user_embeddings"),
    "Courses": client.get_collection("course_embeddings"),
    "Assignments": client.get_collection("submission_embeddings"),
    "Forum Posts": client.get_collection("forum_post_embeddings")
}

# Count stored records
counts = {label: col.count() for label, col in collections.items()}

# 🔍 Query type detection
def detect_relevant_collections(query):
    query = query.lower()
    matched = []

    if any(word in query for word in ["student", "user", "name", "email", "department"]):
        matched.append("Users")
    if any(word in query for word in ["course", "subject", "module", "class"]):
        matched.append("Courses")
    if any(word in query for word in ["assignment", "submission", "submit", "graded"]):
        matched.append("Assignments")
    if any(word in query for word in ["forum", "discussion", "post", "thread"]):
        matched.append("Forum Posts")

    return matched if matched else list(collections.keys())

# 🧠 Ask LLaMA in a loop
while True:
    query = input("\n🧠> ").strip()
    if query.lower() == "exit":
        print("👋 Goodbye!")
        break

    # Set result limit based on query type
    broad_query = any(word in query.lower() for word in ["list", "show all", "get all", "students from", "give me", "total", "count", "how many"])
    match = re.search(r"\b(\d+)\b", query)
    limit = int(match.group(1)) if match else (100 if broad_query else 3)

    query_embedding = model.encode([query])[0]

    # Filter collections
    relevant_labels = detect_relevant_collections(query)
    context_sections = []

    for label in relevant_labels:
        collection = collections[label]
        try:
            results = collection.query(query_embeddings=[query_embedding], n_results=limit)
            documents = results["documents"][0]
            cleaned_docs = [doc.strip().replace("\n", " ") for doc in documents if doc]
            if cleaned_docs:
                section = f"\n# {label} (Total Records: {counts[label]}):\n" + "\n".join(cleaned_docs)
                context_sections.append(section)
        except Exception as e:
            context_sections.append(f"# {label}:\n[Error fetching data: {e}]")

    # Combine all context
    context = "\n".join(context_sections) if context_sections else "No relevant context was found."

    # Final prompt
    prompt = f"""
You are a helpful assistant analyzing Moodle data.

User Query: "{query}"

Here is the retrieved context from the Moodle system:
{context}

Please answer the user query above in a clear, friendly, human-like tone. If the user asks for totals or lists, make sure to reference all available records. If context is missing, politely say so.
"""

    # 🔥 Run LLaMA
    process = subprocess.Popen(["ollama", "run", "llama3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate(prompt)

    print("\n🤖 LLaMA says:\n")
    print(output)
    print("\nAsk another question or type 'exit'.")
