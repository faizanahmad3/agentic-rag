
---

# **Agentic RAG Application**

An **Agentic Retrieval-Augmented Generation (RAG)** application that allows users to upload PDFs, ask questions, and receive accurate answers **with citations (file name + page number)**. The agent uses **multi-step reasoning**, integrates **summarization**, supports **chat memory**, and handles **Arabic queries with concise explanations**.

---

## **Features**

* **Document Upload & Ingestion**

  * Extracts text & metadata (file name, page number)
  * Stores embeddings in **Qdrant Vector Database**

* **Agentic RAG**

  * Uses **LlamaIndex OpenAIAgent** with tools:

    * **DocumentSearch** (retrieval from Qdrant)
    * **DocumentSummarizer** (overview of uploaded docs)

* **Memory**

  * Chat memory for multi-turn contextual conversations

* **Arabic Query Handling**

  * Automatically responds with detailed explanations if input is in Arabic

* **Streamlit Interface**

  * File upload
  * Chat box with answers and citations
  * Buttons to clear database and reset memory

* **Dockerized Setup**

  * One command to run both app and Qdrant via Docker Compose

---

## **Tech Stack**

* **Language:** Python 3.12
* **Frameworks:** LlamaIndex, Streamlit
* **Vector Store:** Qdrant
* **LLM & Embeddings:** OpenAI (GPT-4o + text-embedding-3-small)
* **Containerization:** Docker + Docker Compose

---

## **Project Structure**

```
agentic-rag-app/
│
├── src/
│   ├── agent/               # Agent creation with tools
│   ├── ingestion/           # PDF loader
│   ├── indexing/            # Index builder (Qdrant)
│   ├── retrieval/           # Query engines (retrieval + summarizer)
│   ├── tools/               # Qdrant helper, summarizer
│   └── utils/               # Config, LLM setup
│
├── Documents/                    # Uploaded PDFs
├── Dockerfile               # Streamlit app container
├── docker-compose.yml       # App + Qdrant setup
├── requirements.txt
├── .env.example             # Environment variables template
└── README.md
```

---

## **Setup Instructions**

### **1. Clone Repository**

```bash
git clone https://github.com/faizanahmad3/agentic-rag.git
cd agentic-rag
```

---

### **2. Create `.env` File**

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_key_here
QDRANT_HOST=qdrant
QDRANT_PORT=6333
```

---

### **3. Build & Run with Docker Compose**

```bash
docker-compose up --build
```

* Streamlit App: [http://localhost:8501](http://localhost:8501)
* Qdrant Dashboard: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

---

## **Usage**

1. Open the Streamlit app

2. Upload one or more PDF files

3. Click **Process Documents** (vectors stored in Qdrant)

4. Ask questions in the chat box:

   * Retrieval: *"What is Vision 2030?"*
   * Summarization: *"Summarize all documents"*
   * Arabic: *"ما هي رؤية 2030؟"* → brief explanation

5. **Clear Database** button resets Qdrant collection

6. Chat memory persists until page refresh or manual reset

---

## **Development Setup (Without Docker)**

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Qdrant locally:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Run Streamlit app:

```bash
streamlit run src/ui/app.py
```

---

## **Architecture Overview**

* **Ingestion Phase**

  * Load PDFs → Chunk text → Generate embeddings → Store in Qdrant

* **Agentic Query Phase**

  * User query → Agent decides:

    * Retrieval (DocumentSearch)
    * Summarization (DocumentSummarizer)
  * Combines results → LLM generates answer with citations

* **Memory**

  * Conversation context stored in `ChatMemoryBuffer`

---

## **Special Prompt Behavior**

* Always provide **citations** (file name + page number)
* If query contains **Arabic characters**, respond detailed in Arabic
* Return **“No answer found”** if nothing relevant is retrieved

---

## **Deployment Options**

* **Streamlit Cloud**

  * Use Qdrant Cloud (free tier) for vector storage
* **Render/Railway**

  * Deploy via Dockerfile or Compose
* **Local Demo**

  * Provide `docker-compose.yml` and screen recording

---