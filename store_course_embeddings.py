import json
import chromadb
from sentence_transformers import SentenceTransformer

print("[🚀] Loading model...")
model = SentenceTransformer("BAAI/bge-base-en-v1.5")  # 384-dim
print(f"[ℹ️] Model dimension: {model.get_sentence_embedding_dimension()}")

client = chromadb.PersistentClient(path="chromadb_store")

# 🔁 Always delete old collection (force clean)
print("[🧹] Resetting 'course_embeddings' collection...")
try:
    client.delete_collection(name="course_embeddings")
except:
    pass

collection = client.get_or_create_collection(name="course_embeddings")

# 📂 Load data
with open("mdl_course_text.json", "r") as f:
    data = json.load(f)

# 🧠 Store in batches
batch_size = 1000
for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size]
    texts = [item["text"] for item in batch]
    ids = [f"course_{item['id']}" for item in batch]
    embeddings = model.encode(texts).tolist()
    metadatas = [
        {
            "fullname": item.get("fullname", ""),
            "shortname": item.get("shortname", ""),
            "startdate": item.get("startdate", "")
        } for item in batch
    ]
    collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)

print(f"[✅] Stored {len(data)} course embeddings.")

