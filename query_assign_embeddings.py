import chromadb
from sentence_transformers import SentenceTransformer
import re
import html

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chromadb_store")
collection = client.get_or_create_collection(name="submission_embeddings")

# Load embedding model
print("[~] Loading BGE base model (768D)...")
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Get semantic query
query = input("\n🔍 Enter a semantic assignment query: ")

# Set result limit (default to 5, unless user specifies a number)
match = re.search(r"\b(\d+)\b", query)
limit = int(match.group(1)) if match else 5

# Generate query embedding
query_embedding = model.encode([query])[0]

# Query ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=limit
)

# Debug: print raw result object
#print("\n[DEBUG] Raw ChromaDB result:\n", results)

# Display cleaned results
print("\n📌 Matching Assignment Submissions:\n")
for i, doc in enumerate(results["documents"][0], 1):
    cleaned_text = html.unescape(re.sub(r"<[^>]+>", "", doc))
    print(f"{i}. {cleaned_text.strip()}\n")

