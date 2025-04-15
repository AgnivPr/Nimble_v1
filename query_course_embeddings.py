import json
import re
import html
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize ChromaDB client and collection
client = chromadb.PersistentClient(path="chromadb_store")
collection = client.get_or_create_collection(name="course_embeddings")

# Load the embedding model
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Ask for query input
query = input("🔍 Enter a semantic course query: ")

# Convert the query to embedding
query_embedding = model.encode([query]).tolist()

# Perform the query
results = collection.query(query_embeddings=query_embedding, n_results=100, include=["metadatas", "documents"])

# Clean HTML tags and entities
def clean_text(text):
    no_html = re.sub(r"<.*?>", "", text)
    return html.unescape(no_html)

# Extract limit from query if user specifies a number (like "5 Python courses")
match = re.search(r"(\d+)", query)
limit = int(match.group(1)) if match else len(results["documents"][0])

# Display results
print("\n📌 Matching Courses:\n")
for i in range(limit):
    metadata = results["metadatas"][0][i]
    description = clean_text(results["documents"][0][i])
    course_name = metadata.get("fullname", "Unknown Course")

    print(f"{i+1}. {course_name}")
    print(f"   {description}\n")

