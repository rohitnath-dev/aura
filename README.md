<p align="center">
  <img src="./assets/aura-logo.png" width="220">
</p>

<h1 align="center">AURA</h1>

<p align="center">
  <strong>Persistent AI Personalities</strong>
</p>

<p align="center">
  Memory • Identity • Continuity
</p>

<p align="center">
  AI personalities with memory, identity, and long-term continuity.
</p>

<p align="center">
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-MVP-blueviolet">
  <img src="https://img.shields.io/badge/Frontend-React-61DAFB">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688">
  <img src="https://img.shields.io/badge/Memory-FAISS-4CAF50">
</p>

---

## Overview

AURA is an AI clone platform focused on creating persistent digital personalities that can remember information, retrieve relevant context, and interact consistently over time.

The project combines conversational AI, retrieval-based memory systems, and personality-driven interactions to explore long-term AI identity and continuity.

---

## Current Capabilities

- Clone creation workflow
- Conversational AI interface
- Memory retrieval system
- Retrieval-Augmented Generation (RAG)
- OpenRouter model integration
- FastAPI backend
- React frontend

---

## Repository Structure

```
ai-clone-platform/
│
├── backend/
│   ├── processed_data/
│   ├── faiss_index/
│   ├── core/
│   ├── rag.py
│   ├── server.py
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── public/
│   ├── src/
│   └── ...
│
├── users/
│   └── ...
│
├── .gitignore
└── README.md
```

---

## Architecture

```
Frontend
    │
    ▼
FastAPI Backend
    │
    ▼
Memory & Retrieval Layer
    │
    ▼
FAISS Vector Search
    │
    ▼
OpenRouter Models
```

---

## Tech Stack

### Frontend

- React
- Vite
- React Router

### Backend

- FastAPI
- Python

### AI & Memory

- LangChain
- LangGraph
- FAISS
- Sentence Transformers
- OpenRouter

---

## Local Setup

### Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate
# Windows:
# venv\Scripts\activate

pip install -r requirements.txt

uvicorn server:server --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

## API

### Health Check

**GET** `/`

---

### Chat

**POST** `/chat`

Example:

```json
{
  "message": "Hello"
}
```

---

## Development Notes

- Frontend and backend run independently during development.
- Backend services must be available for chat functionality.
- Memory retrieval is powered by FAISS vector search.
- Model responses are generated through OpenRouter integrations.
- The project is under active development and internal experimentation.

---

## Status

**Current Stage:** MVP Development

---

## License

Private Repository
Internal Use Only
