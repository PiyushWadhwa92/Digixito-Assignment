# Legal RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that helps users identify the applicable Indian criminal law provisions for everyday legal scenarios. Built with Streamlit for the frontend and Python for the backend logic.

## Table of Contents

- [About the Project](#about-the-project)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Configuration](#configuration)
- [Sample Questions](#sample-questions)
- [Architecture Overview](#architecture-overview)
- [Future Scope](#future-scope)
- [Author](#author)

---

## About the Project

In India, many citizens are unaware of which specific law or section applies when they become victims of a crime. This chatbot was built to bridge that gap. A user simply describes their situation in plain English (for example, "Someone stole my phone at the metro station"), and the chatbot responds with:

- **Crime Category** — what type of crime it is
- **Applicable Law** — which act or statute governs the offense
- **Relevant Section** — the specific section number, if applicable
- **Explanation** — a brief description of the legal provision
- **Justification** — why this particular section applies to the user's situation

The system currently covers 15 common crime categories including theft, cyber fraud, assault, identity theft, domestic violence, murder, hacking, kidnapping, and more. It also supports an optional OpenAI integration for handling queries that fall outside the built-in knowledge base.

## How It Works

The chatbot follows a simple RAG-inspired pipeline:

1. **User Query** — The user types a legal question in the Streamlit chat interface.
2. **Document Retrieval** — The system searches through stored legal documents (`.txt` files in the `data/` folder) using cosine similarity on pseudo-embeddings. The top-k most relevant documents are returned as context.
3. **Response Generation** — The query is matched against a keyword-based knowledge base of 15 legal scenarios. If a match is found, a structured legal response is returned. If no match is found and the OpenAI integration is enabled, the query is forwarded to the LLM for a more nuanced answer.
4. **Formatted Output** — The response is displayed in a clean, structured format with bold headings for each field.

## Project Structure

```
legal-rag-chatbot/
│
├── app.py                  # Main Streamlit application (entry point)
├── requirements.txt        # Python dependencies
├── setup.ps1               # PowerShell script for quick setup
├── build_faiss.py          # Script to build a FAISS vector index (optional)
├── .env.example            # Template for environment variables
│
├── assets/
│   └── custom.css          # Custom dark-theme CSS for the Streamlit UI
│
├── data/                   # Place your legal documents (.txt) here
│
├── utils/
│   ├── __init__.py
│   ├── chatbot.py          # Orchestrates retrieval + response generation
│   ├── embeddings.py       # Pseudo-embedding functions for document similarity
│   ├── llm.py              # Rule-based response engine + OpenAI fallback
│   └── vectorstore.py      # Lightweight cosine similarity search over documents
│
├── vectorstore/            # Stores FAISS index files (if generated)
├── sample_cases/           # Sample legal case documents
└── architecture/           # Architecture diagrams (if any)
```

## Tech Stack

| Component       | Technology                     |
|-----------------|--------------------------------|
| Frontend        | Streamlit 1.38.0               |
| Language        | Python 3.11                    |
| Embeddings      | NumPy-based pseudo-embeddings  |
| Vector Search   | Cosine similarity (custom) / FAISS (optional) |
| LLM (optional)  | OpenAI API (gpt-4o-mini)       |
| Orchestration   | LangChain 0.2.8                |
| Styling         | Custom CSS (dark theme)        |

## Getting Started

### Prerequisites

- **Python 3.11** or higher installed on your system
- **pip** (comes bundled with Python)
- A terminal or PowerShell window



## Sample Questions

Here are some questions you can try in the chatbot. These are the same scenarios used during development and testing.

| # | Question | Expected Crime Category |
|---|----------|------------------------|
| 1 | Someone stole my mobile phone from the railway station. | Theft |
| 2 | I clicked on a fake payment link and money was deducted from my account. | Cyber Fraud |
| 3 | My neighbor attacked me and caused injuries during a fight. | Assault / Causing Hurt |
| 4 | Someone created a fake Instagram account using my name and photos. | Identity Theft |
| 5 | A woman is facing physical abuse from her husband at home. | Domestic Violence |
| 6 | A person was driving after drinking alcohol and hit another car. | Drunk Driving |
| 7 | A man intentionally killed another person using a knife. | Murder |
| 8 | Someone is threatening to leak my private photos unless I send money. | Cyber Blackmail / Extortion |
| 9 | A fraudster called pretending to be a bank employee and stole my OTP. | Banking Fraud |
| 10 | A child was taken away forcefully by unknown people. | Kidnapping |
| 11 | Someone hacked my email account and changed the password. | Unauthorized Access / Hacking |
| 12 | My car windows were broken intentionally by a group of people. | Mischief / Property Damage |
| 13 | An employee is repeatedly harassed and threatened by the manager. | Workplace Harassment |
| 14 | Two bike riders snatched a gold chain from a woman on the road. | Robbery / Snatching |
| 15 | I paid money for a job offer but later found the company was fake. | Job Scam / Cheating |

## Architecture Overview

```
┌────────────────────┐
│   Streamlit UI     │  ←  User types a legal question
│   (app.py)         │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│   chatbot.py       │  ←  Orchestrates the pipeline
│   get_answer()     │
└───┬────────────┬───┘
    │            │
    ▼            ▼
┌──────────┐ ┌──────────────┐
│vectorstore│ │   llm.py      │
│get_top_k()│ │get_response() │
└──────────┘ └───────┬───────┘
    │                │
    ▼                ▼
┌──────────┐ ┌──────────────┐
│embeddings│ │ Rule-based   │
│  .py     │ │ _ANSWER_DB   │
│(cosine   │ │      OR      │
│ search)  │ │ OpenAI API   │
└──────────┘ └──────────────┘
```

**Flow:**
1. `app.py` receives the user query and calls `chatbot.get_answer()`.
2. `chatbot.py` does two things in parallel:
   - Retrieves top-k relevant documents from the `data/` folder using cosine similarity (`vectorstore.py` + `embeddings.py`).
   - Generates a structured legal response using the rule-based engine in `llm.py`.
3. If no rule-based match is found and `USE_REAL_LLM=True`, the query is sent to the OpenAI API.
4. The answer and retrieved sources are displayed back in the Streamlit UI.

## Future Scope

- **Expand the knowledge base** — Add more crime categories and edge cases to the rule-based engine.
- **Integrate a production LLM** — Use GPT-4 or an open-source model like LLaMA for handling arbitrary legal questions.
- **Add real embeddings** — Replace the pseudo-embeddings with a proper Sentence Transformer model (e.g., `all-MiniLM-L6-v2`) for more accurate document retrieval.
- **Upload legal PDFs** — Allow users to upload their own legal documents for retrieval.
- **Multi-language support** — Add Hindi and regional language support for wider accessibility.
- **Deployment** — Host on Streamlit Cloud, AWS, or Heroku for public access.

## Author

Built as part of the GenAI Assignment.

---

> **Note:** This project is intended for educational and demonstration purposes only. It does not constitute legal advice. For real legal matters, please consult a qualified lawyer.
