import os
import json
import requests

from pathlib import Path
from typing import List, TypedDict

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

from langgraph.graph import StateGraph, START, END

from core.memory_manager import (
    save_message,
    get_last_messages,
    load_summary,
    save_summary,
    count_messages
)


load_dotenv(".env")


class OpenRouterLLM:

    def __init__(self, model="openai/gpt-4o-mini"):

        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found")

        self.model = model

        self.url = "https://openrouter.ai/api/v1/chat/completions"

    def invoke(self, system_prompt, user_prompt):

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        }

        try:

            response = requests.post(
                self.url,
                headers=headers,
                json=data,
                timeout=120
            )

            result = response.json()

            return result["choices"][0]["message"]["content"]

        except Exception as e:

            print("LLM ERROR:")
            print(e)

            return "Something went wrong while generating the response."


llm = OpenRouterLLM()


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


retriever_cache = {}


class State(TypedDict):

    username: str
    question: str

    docs: List[Document]

    context: str
    history: str
    summary: str

    answer: str


BASE_DIR = Path(__file__).resolve().parent

SYSTEM_PROMPT_PATH = (
    BASE_DIR / "prompts" / "system_prompt.txt"
)

MEMORY_RULES_PATH = (
    BASE_DIR / "prompts" / "memory_handling_rules.txt"
)

with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

with open(MEMORY_RULES_PATH, "r", encoding="utf-8") as f:
    MEMORY_RULES = f.read()


FINAL_SYSTEM_PROMPT = f"""
{SYSTEM_PROMPT}

==================================================

{MEMORY_RULES}
"""


def load_user_retriever(username):

    if username in retriever_cache:
        return retriever_cache[username]

    processed_file = (
        f"../users/{username}/"
        f"processed_data/processed_user_data.json"
    )

    if not os.path.exists(processed_file):
        return None

    try:

        with open(processed_file, "r", encoding="utf-8") as f:
            data = json.load(f)

    except Exception as e:

        print("FAILED TO LOAD USER DATA:")
        print(e)

        return None

    docs = []

    for item in data:

        text = item.get("text", "").strip()

        if not text:
            continue

        docs.append(
            Document(
                page_content=text,
                metadata={
                    "source": item.get("source", "unknown"),
                    "type": item.get("type", "unknown")
                }
            )
        )

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100
    ).split_documents(docs)

    vector_db_path = (
        f"../users/{username}/faiss_index"
    )

    os.makedirs(vector_db_path, exist_ok=True)

    try:

        if os.path.exists(
            os.path.join(vector_db_path, "index.faiss")
        ):

            vector_store = FAISS.load_local(
                vector_db_path,
                embeddings,
                allow_dangerous_deserialization=True
            )

        else:

            vector_store = FAISS.from_documents(
                chunks,
                embeddings
            )

            vector_store.save_local(vector_db_path)

        retriever = vector_store.as_retriever(
            search_kwargs={"k": 6}
        )

        retriever_cache[username] = retriever

        return retriever

    except Exception as e:

        print("FAISS ERROR:")
        print(e)

        return None


def retrieve(state: State):

    username = state["username"]

    retriever = load_user_retriever(username)

    if retriever is None:

        return {
            **state,
            "docs": []
        }

    try:

        retrieved_docs = retriever.invoke(
            state["question"]
        )

    except Exception as e:

        print("RETRIEVAL ERROR:")
        print(e)

        retrieved_docs = []

    return {
        **state,
        "docs": retrieved_docs
    }


def generate_summary(username):

    try:

        messages = get_last_messages(
            username=username,
            limit=50
        )

        if not messages:
            return

        history_text = "\n".join(
            [
                f"{msg[0]}: {msg[1]}"
                for msg in messages
            ]
        )

        prompt = f"""
Summarize these conversations into persistent long-term memory.

Keep:
- goals
- personality
- important discussions
- ongoing projects
- emotional patterns
- preferences

Conversation:
{history_text}
"""

        summary = llm.invoke(
            system_prompt="You generate memory summaries.",
            user_prompt=prompt
        )

        save_summary(username, summary)

    except Exception as e:

        print("SUMMARY ERROR:")
        print(e)


def generate_from_context(state: State):

    username = state["username"]
    question = state["question"]

    messages = get_last_messages(
        username=username,
        limit=10
    )

    history = "\n".join(
        [
            f"{msg[0].upper()}: {msg[1]}"
            for msg in messages
        ]
    ).strip()

    if not history:
        history = "No previous conversation."

    summary = load_summary(username)

    if not summary:
        summary = "No long-term memory yet."

    context_parts = []

    for d in state.get("docs", []):

        source = d.metadata.get(
            "source",
            "unknown"
        )

        doc_type = d.metadata.get(
            "type",
            "unknown"
        )

        content = d.page_content.strip()

        if not content:
            continue

        context_parts.append(
            f"""
SOURCE: {source}

TYPE: {doc_type}

CONTENT:
{content}
""".strip()
        )

    context = "\n\n====================\n\n".join(
        context_parts
    ).strip()

    if not context:
        context = "No relevant memory found."

    user_prompt = f"""
You are talking naturally with the user.

Use:
1. Personality memory
2. Long-term memory
3. Conversation history

Behave like a real persistent human identity.

Never say:
- I don't remember
- I can't access previous chats

========================================
PERSONALITY MEMORY
========================================

{context}

========================================
LONG TERM MEMORY
========================================

{summary}

========================================
RECENT CONVERSATION
========================================

{history}

========================================
CURRENT USER MESSAGE
========================================

{question}
""".strip()

    try:

        out = llm.invoke(
            system_prompt=FINAL_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )

        out = out.strip()

    except Exception as e:

        print("GENERATION ERROR:")
        print(e)

        out = (
            "Something went wrong while "
            "generating the response."
        )

    save_message(
        username=username,
        role="user",
        content=question
    )

    save_message(
        username=username,
        role="assistant",
        content=out
    )

    try:

        total_messages = count_messages(username)

        if total_messages % 30 == 0:
            generate_summary(username)

    except Exception as e:

        print("SUMMARY CHECK ERROR:")
        print(e)

    return {
        **state,
        "answer": out,
        "context": context,
        "history": history,
        "summary": summary
    }


g = StateGraph(State)

g.add_node(
    "retrieve",
    retrieve
)

g.add_node(
    "generate_from_context",
    generate_from_context
)

g.add_edge(
    START,
    "retrieve"
)

g.add_edge(
    "retrieve",
    "generate_from_context"
)

g.add_edge(
    "generate_from_context",
    END
)

app = g.compile()
