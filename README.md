# 🎓 PlaceWise — AI-Powered Placement Assistant

> Ask questions about college placement history in plain English. Get accurate, source-cited answers — grounded in official records, not guesswork.

**Live Demo:** [Add your Streamlit link here once deployed]

---

## 📌 The Problem

Final-year students struggle to get quick, accurate answers about placement history. Data is scattered across multiple yearly PDFs on the college website — hard to search, easy to misread, and impossible to query naturally. Students often end up relying on outdated peer hearsay instead of official records.

## 💡 The Solution

**PlaceWise** combines a conversational AI assistant with a live analytics dashboard, both powered by the same underlying placement data. Ask a question like *"How many offers did Amazon give across the years?"* and get a direct, accurate answer — complete with citations showing exactly which official document it came from.

Unlike a typical chatbot demo, PlaceWise:
- **Never hallucinates** — it only answers from retrieved, real document content
- **Remembers conversations** — persistent chat history across sessions
- **Visualizes the data** — a built-in analytics dashboard, not just Q&A

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **RAG-based Q&A** | Natural language questions, answered from real placement PDFs |
| 📎 **Source Citations** | Every answer shows which document(s) it came from |
| 💬 **Persistent Chat History** | Conversations saved across sessions via SQLite |
| 📊 **Analytics Dashboard** | Live charts: top recruiters, offers by year, searchable company data |
| 🎯 **Adaptive Retrieval** | Automatically adjusts search depth for broad vs. specific questions |
| 🎨 **Custom UI** | Structured, premium interface — not default Streamlit styling |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| PDF Extraction | `pdfplumber` (table-aware extraction) |
| Text Chunking | LangChain `RecursiveCharacterTextSplitter` |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) — local, free |
| Vector Database | ChromaDB |
| LLM | Groq API (`openai/gpt-oss-120b`) |
| Data Analytics | `pandas` + regex-based entity normalization |
| Persistent Storage | SQLite |
| Frontend | Streamlit + custom CSS |

**100% free stack** — no paid APIs, no paid hosting.

---

## 📊 Evaluation

Tested against 12 real questions spanning direct lookups, multi-year comparisons, and edge cases.

| Query Type | Accuracy |
|---|---|
| Direct lookups (e.g., "How many offers did Wipro give?") | ~90%+ |
| Broad/exhaustive queries (e.g., "List all IT companies") | ~58% → improved after fix |

**Key finding:** Broad queries initially underperformed because a fixed retrieval depth (`top_k=4`) sometimes missed relevant chunks scattered across the document set. 

**Fix implemented:** Adaptive retrieval — the system now detects broad/exhaustive question patterns (keywords like "all," "every," "total," "compare") and automatically increases retrieval depth for those queries, while keeping direct lookups fast.

---

## 🖼️ Screenshots

*(Add 2-3 screenshots here — chat interface, insights dashboard)*

---

## 🚀 Running Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/placewise.git
cd placewise

# Set up virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Build the vector index (one-time)
python src/embed_store.py
python src/analytics.py

# Run the app
streamlit run app.py
```

---

## 📁 Project Structure
