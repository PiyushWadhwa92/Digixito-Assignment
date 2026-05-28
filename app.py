import streamlit as st
from utils.chatbot import get_answer

st.set_page_config(page_title="Legal RAG Chatbot", layout="centered")

# Apply custom CSS
with open("assets/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("⚖️ Legal RAG Chatbot")
st.caption("Retrieve‑augmented generation for legal queries (placeholder LLM)")

query = st.chat_input("Enter your legal question...")
if query:
    with st.spinner("Processing..."):
        answer, sources = get_answer(query)
    st.markdown(f"**Answer:**\n{answer}")
    if sources:
        with st.expander("Relevant documents"):
            for src in sources:
                st.markdown(f"- {src}")
