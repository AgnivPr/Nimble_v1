# store_assign_submission_embeddings.py

import json
import chromadb
from sentence_transformers import SentenceTransformer

# NEW ChromaDB initialization
client = chromadb.PersistentClient(path="chromadb_store")

# Load BGE embedding model
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Load assignment submission data
with open("mdl_assign_submission_text.json", "r") as f:
    data = json.load(f)

# Create or get collection
collection = client.get_or_create_collection(name="submission_embeddings")

# Prepare texts and IDs
texts = [item["text"] for item in data]
ids = [f"submission_{item['id']}" for item in data]

# Generate embeddings
embeddings = model.encode(texts, batch_size=64, show_progress_bar=True).tolist()

# Add to ChromaDB in batches
batch_size = 40000
for i in range(0, len(texts), batch_size):
    batch_texts = texts[i:i+batch_size]
    batch_ids = ids[i:i+batch_size]
    batch_embeddings = embeddings[i:i+batch_size]
    
    collection.add(documents=batch_texts, embeddings=batch_embeddings, ids=batch_ids)
    print(f"[✓] Stored batch {i//batch_size + 1} ({len(batch_texts)} items)")

print(f"[✅] Finished storing {len(texts)} assignment submission embeddings to ChromaDB.")

