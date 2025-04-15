import chromadb

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="rag_embeddings")

# Fetch all stored records
records = collection.get()

# Print results
print("Stored Data in ChromaDB:", records)
print("Total Records Stored:", len(records["ids"]))  # Count stored IDs

