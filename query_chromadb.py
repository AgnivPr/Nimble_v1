import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("BAAI/bge-small-en")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="rag_embeddings")

print("Type a search query (e.g., 'What is deep learning?')")
print('Type "exit" to quit the script.\n')

while True:
    query = input("Enter your query: ").strip()
    if query.lower() == "exit":
        break

    # Generate embedding for the query
    query_embedding = model.encode(query).tolist()

    # Retrieve only the most relevant result (n_results=1)
    results = collection.query(query_embeddings=[query_embedding], n_results=1)

    # Check if results exist
    if results and results["documents"] and results["documents"][0]:
        most_relevant_doc = results["documents"][0][0]  # Get the most relevant document
        print("\n🔍 **Most Relevant Result:**")
        print(f"✅ {most_relevant_doc}\n")
    else:
        print("\n❌ No relevant results found.\n")

