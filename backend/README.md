# AURA Backend

Backend services powering memory, retrieval, and AI interaction within AURA.

---

## Overview

The AURA backend is responsible for:

- AI response generation
- memory management
- retrieval pipelines
- vector search
- user data processing
- API endpoints
- clone orchestration

The backend acts as the central intelligence layer between the frontend interface, memory systems, and language models.

---

## Responsibilities

### AI Layer

- OpenRouter integration
- prompt construction
- response generation
- model routing

### Memory Layer

- conversation storage
- memory retrieval
- semantic search
- memory processing

### Retrieval Layer

- FAISS vector indexing
- similarity search
- context retrieval
- RAG pipeline

### API Layer

- FastAPI server
- request handling
- response delivery

---

## Structure

```
backend/
│
├── core/
│   └── ...
│
├── processed_data/
│   └── ...
│
├── faiss_index/
│   └── ...
│
├── users/
│   └── ...
│
├── rag.py
├── server.py
├── requirements.txt
└── .env
```

---

## Setup

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the backend directory.

```
OPENROUTER_API_KEY=your_api_key_here
```

---

## Running the Server

```bash
uvicorn server:server --reload
```

**Server:** http://127.0.0.1:8000

---

## Core Concepts

### Retrieval-Augmented Generation (RAG)

User messages are enriched with relevant retrieved memories before being sent to the language model.

### Vector Search

Semantic memory retrieval is powered by FAISS vector indexes.

### Memory Persistence

User-related information is stored and processed to maintain conversational continuity.

---

## Development Notes

- Backend must be running before frontend chat functionality can operate.
- FAISS indexes are generated and stored locally.
- Memory retrieval quality directly impacts response quality.
- The architecture is expected to evolve as AURA's memory systems mature.

---

## Status

**Active Development**

Internal Use Only
