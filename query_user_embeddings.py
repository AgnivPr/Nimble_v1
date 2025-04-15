# query_user_embeddings.py

import chromadb
from sentence_transformers import SentenceTransformer
import re
import html

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chromadb_store")
collection = client.get_or_create_collection(name="user_embeddings")

# Load embedding model
print("[~] Loading BGE base model (768D)...")
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Get semantic query from user
query = input("\n🔍 Enter a semantic user query: ")

# Try to extract an optional number (e.g., "show 5 students...")
match = re.search(r"\b(\d+)\b", query)
limit = int(match.group(1)) if match else 1  # ✅ default to 1 if no number found

# Generate embedding
query_embedding = model.encode([query])[0]

# Query ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=limit
)

# Show results
print("\n🎯 Matching Users:\n")
for i, doc in enumerate(results['documents'][0], 1):
    cleaned_text = html.unescape(re.sub(r"<[^>]+>", "", doc))
    print(f"{i}. {cleaned_text.strip()}\n")

