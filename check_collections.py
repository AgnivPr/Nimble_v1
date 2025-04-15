import chromadb

client = chromadb.PersistentClient(path="./chroma_db")  
collections = client.list_collections()

# New way to access collection names in Chroma v0.6.0
collection_names = [col for col in collections]  

print("Available Collections:", collection_names)

