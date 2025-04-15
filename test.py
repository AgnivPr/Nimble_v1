python -c "
import chromadb
client = chromadb.PersistentClient(path='./chroma_db')
collection = client.get_collection(name='rag_embeddings')
print(collection.peek(limit=3))  # Show a few stored records
"
