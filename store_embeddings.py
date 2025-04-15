# store_embeddings.py

import json
import chromadb
from sentence_transformers import SentenceTransformer

# Load text data
with open("mdl_user_text.json", "r") as f:
    data = json.load(f)

# Extract texts for embedding
texts = [entry["text"] for entry in data]

# Load BGE embedding model
print("[~] Loading embedding model...")
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# Generate embeddings
print("[~] Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="rag_embeddings")

# Store data
print("[~] Storing embeddings in ChromaDB...")
collection.add(
    documents=texts,
    embeddings=embeddings,
    ids=[str(i) for i in range(len(texts))],
    metadatas=[{"text": text} for text in texts]
)

print(f"[✓] Stored {len(texts)} records in ChromaDB!")

