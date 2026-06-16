# Agentic AI with GDC

A multi-agent AI system combining **Google ADK**, **LangGraph**, and **Groq** to deliver finance assistance, investment planning, booking status, and RAG-based document Q&A.

---

## Project Structure

```
Agentic_AI_with_GDC/
├── finance_assistant_agent/    # Root agent — orchestrates finance & investment tools
│   └── agent.py
├── investment_plan_agent/      # Sub-agent — searches live investment options via Google Search
│   └── agent.py
├── resources/
│   └── sample.pdf              # Source PDF for RAG pipeline
├── chunker.py                  # Splits PDF text into overlapping chunks
├── dataprocessor.py            # Orchestrates PDF extraction → chunking → embedding → Pinecone
├── embedder.py                 # Generates embeddings using HuggingFace (all-MiniLM-L6-v2)
├── vectorstore.py              # Upserts embeddings into Pinecone index
├── llmdemo.py                  # RAG demo — queries Pinecone + answers via Groq LLM
├── architecture.html           # Interactive architecture diagram (open in browser)
├── requirements.txt
└── .env
```

---

## Agents

### finance_assistant_agent (root)
- Built with **Google ADK** `LlmAgent` + `gemini-2.5-flash`
- Tools:
  - `get_user_finance_details` — returns user salary, expenses, investments, debts, risk appetite, and goals
  - `investment_plan_agent` — delegates to the investment sub-agent via `AgentTool`

### investment_plan_agent
- Built with **Google ADK** `LlmAgent` + `gemini-2.5-flash`
- Tools:
  - `google_search` — fetches live investment options based on user financial profile

---

## RAG Pipeline (`llmdemo.py`)

```
PDF → chunker.py → embedder.py → vectorstore.py (Pinecone)
                                        ↓
              user query → embed → Pinecone search → Groq LLM → answer
```

| Step | File | Description |
|------|------|-------------|
| 1 | `dataprocessor.py` | Extract text from PDF, chunk, embed, store in Pinecone |
| 2 | `llmdemo.py` | Embed user query, retrieve top-k matches, generate answer via Groq |

---

## Setup

### 1. Python Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=<your_google_api_key>
GROQ_API_KEY=<your_groq_api_key>
PINECONE_API_KEY=<your_pinecone_api_key>
PINECONE_INDEX_NAME=<your_pinecone_index_name>
```

---

## Running the Agents

### Finance Assistant Agent (Google ADK)
```bash
adk run finance_assistant_agent
```

Or launch the ADK web UI:
```bash
adk web
```

### RAG Pipeline

**Step 1 — Process and index the PDF:**
```bash
python dataprocessor.py
```

**Step 2 — Query the RAG system:**
```bash
python llmdemo.py
```

---

## Architecture

Open `architecture.html` in a browser to view the full interactive diagram.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `google-adk` | Agent framework for finance & investment agents |
| `langchain-google-genai` | Google Generative AI embeddings |
| `langchain-groq` | Groq LLM integration |
| `langgraph` | ReAct agent runtime |
| `pinecone` | Vector database for RAG |
| `sentence-transformers` | HuggingFace embedding model |
| `PyPDF2` | PDF text extraction |
| `python-dotenv` | Environment variable management |
