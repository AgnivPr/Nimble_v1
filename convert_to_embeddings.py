import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# Load extracted text data
df = pd.read_csv("extracted_data.csv")  # Ensure this file exists
texts = df["combined_text"].dropna().tolist()  # Remove empty values

print("Loaded", len(texts), "records for embedding.")  # Debugging purpose

# Load BGE model
model = SentenceTransformer("BAAI/bge-small-en")  # Use bge-base-en or bge-large-en for better accuracy

# Enable better retrieval quality
instruction = "Represent this sentence for retrieval: "
texts = [instruction + text for text in texts]  # Add instruction for embedding quality

# Generate embeddings
embeddings = model.encode(texts, normalize_embeddings=True)  # Normalize for better similarity search

# Convert to NumPy array
embeddings = np.array(embeddings)

print("Generated Embeddings Shape:", embeddings.shape)  # Debugging

# Save embeddings
np.save("bge_embeddings.npy", embeddings)
df.to_csv("embedded_data.csv", index=False)  # Save text with embeddings

print("Embeddings saved successfully as bge_embeddings.npy")

