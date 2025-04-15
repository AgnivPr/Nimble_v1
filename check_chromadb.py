import chromadb

try:
    # Connect to ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")

    # Check available collections
    collections = client.list_collections()
    print("ChromaDB is working! Collections:", collections)

except Exception as e:
    print("Error:", e)
