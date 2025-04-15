import json
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid

# Load assignment data
with open("mdl_assign_text.json", "r") as f:
    assignment_data = json.load(f)

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="chromadb_store")


# Create or get collection
collection = client.get_or_create_collection(name="assignment_embeddings")

# Load BGE embedding model
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Prepare and embed
texts = [item["text"] for item in assignment_data]
ids = [str(uuid.uuid4()) for _ in texts]
embeddings = model.encode(texts).tolist()

# Add to ChromaDB
collection.add(documents=texts, embeddings=embeddings, ids=ids)

print(f"[✓] Stored {len(texts)} assignment embeddings in ChromaDB.")
