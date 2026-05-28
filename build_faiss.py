import os
from utils.embeddings import load_data_files, embed_documents
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_faiss_index(data_dir: str = "data", index_dir: str = "vectorstore/faiss_index"):
    # Load documents (filepath, content)
    docs = load_data_files(data_dir)
    if not docs:
        print("No .txt files found in", data_dir)
        return
    paths, texts = zip(*docs)
    # Initialize deterministic embeddings (placeholder)
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Create FAISS index from texts
    vectorstore = FAISS.from_texts(list(texts), embedding)
    # Ensure index directory exists
    os.makedirs(index_dir, exist_ok=True)
    # Save index locally
    vectorstore.save_local(index_dir)
    print(f"FAISS index saved to {index_dir}")

if __name__ == "__main__":
    build_faiss_index()
