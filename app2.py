import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import subprocess
import re

# Page config
st.set_page_config(page_title="NIMBLE - Moodle Assistant", layout="wide")

# Load embedding model
@st.cache_resource
def load_model():
    return SentenceTransformer("BAAI/bge-base-en-v1.5")

model = load_model()

# Initialize ChromaDB
client = chromadb.PersistentClient(path="chromadb_store")
collections = {
    "Users": client.get_collection("user_embeddings"),
    "Courses": client.get_collection("course_embeddings"),
    "Assignments": client.get_collection("submission_embeddings"),
    "Forum Posts": client.get_collection("forum_post_embeddings")
}
counts = {label: col.count() for label, col in collections.items()}

# App title
st.title("🧠 NIMBLE")
st.caption("Nitte's Intelligent Moodle-Based Learning Engine — powered by LLaMA 3")
st.markdown("---")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_query = st.text_input("🔍 Ask your Moodle Question")

if user_query:
    with st.spinner("Thinking like a Nitte genius... 💭"):
        broad_query = any(word in user_query.lower() for word in ["list", "all", "show", "total", "how many", "get"])
        match = re.search(r"\b(\d+)\b", user_query)
        limit = int(match.group(1)) if match else (100 if broad_query else 3)

        query_embedding = model.encode([user_query])[0]

        # Search in ChromaDB
        context_sections = []
        for label, collection in collections.items():
            try:
                results = collection.query(query_embeddings=[query_embedding], n_results=limit)
                documents = results["documents"][0]
                cleaned_docs = [doc.strip().replace("\n", " ") for doc in documents if doc]
                section = f"\n# {label} (Total Records: {counts[label]}):\n" + "\n".join(cleaned_docs)
                context_sections.append(section)
            except Exception as e:
                context_sections.append(f"# {label}:\n[Error retrieving data: {e}]")

        context = "\n".join(context_sections)

        # LLaMA Prompt for NIMBLE
        prompt = f"""
You are NIMBLE — Nitte's Intelligent Moodle-Based Learning Engine.
You're powered by LLaMA 3 and your role is to help students and faculty get answers from the Moodle system.

User Question: "{user_query}"

Relevant Moodle Data:
{context}

Provide a helpful, friendly, and student-like answer to the user's question using the information available.
"""

        # Execute LLaMA
        process = subprocess.Popen(
            ["ollama", "run", "llama3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, error = process.communicate(prompt)
        answer = output.strip()

        # Save to chat history
        st.session_state.chat_history.append((user_query, answer))

# Display chat history neatly
if st.session_state.chat_history:
    st.markdown("### 💬 Chat History")
    for q, a in reversed(st.session_state.chat_history):
        st.markdown(f"""
        <div style="
            border: 2px solid #007bff;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            background-color: #f8fbff;">
            <strong>🧠 You:</strong> {q}<br><br>
            <strong>🤖 NIMBLE:</strong> {a}
        </div>
        """, unsafe_allow_html=True)

