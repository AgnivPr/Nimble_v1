# store_forum_posts_embeddings.py

import json
import chromadb
from sentence_transformers import SentenceTransformer

# Connect to ChromaDB (new-style client)
client = chromadb.PersistentClient(path="chromadb_store")

# Load BGE embedding model
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Load forum post data
with open("mdl_forum_posts_text.json", "r") as f:
    data = json.load(f)

# Create or get collection
collection = client.get_or_create_collection(name="forum_post_embeddings")

# Prepare texts and IDs
texts = [item["text"] for item in data]
ids = [f"forum_{item['id']}" for item in data]

# Batch add embeddings to avoid ValueError (Chroma limit)
batch_size = 40000
for i in range(0, len(texts), batch_size):
    batch_texts = texts[i:i + batch_size]
    batch_ids = ids[i:i + batch_size]
    batch_embeddings = model.encode(batch_texts).tolist()
    
    collection.add(documents=batch_texts, embeddings=batch_embeddings, ids=batch_ids)
    print(f"[✓] Stored batch {i // batch_size + 1}")

print(f"[✅] Stored total {len(texts)} forum post embeddings to ChromaDB.")
