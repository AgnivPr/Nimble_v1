# embed_mdl_user.py

import json
import chromadb
from sentence_transformers import SentenceTransformer

# Load mdl_user text data
with open("mdl_user_text.json", "r") as f:
    data = json.load(f)

texts = [entry["text"] for entry in data]

# Load BGE base embedding model (768D)
print("[~] Loading BGE base embedding model (768D)...")
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Generate embeddings
print("[~] Generating user embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)

# Connect to ChromaDB (same path as used before)
client = chromadb.PersistentClient(path="chromadb_store")

# Create/replace user_embeddings collection
try:
    client.delete_collection(name="user_embeddings")
except:
    pass  # Ignore if doesn't exist

collection = client.get_or_create_collection(name="user_embeddings")

# Store in ChromaDB
print("[~] Storing user embeddings into ChromaDB...")
collection.add(
    documents=texts,
    embeddings=embeddings,
    ids=[f"user_{i}" for i in range(len(texts))],
    metadatas=[{"text": text} for text in texts]
)

print(f"[✓] Stored {len(texts)} user embeddings (768D) in ChromaDB collection 'user_embeddings'.")
