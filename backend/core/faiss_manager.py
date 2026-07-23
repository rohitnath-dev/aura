import os
import json

from langchain_core.documents import Document

from langchain_community.vectorstores import FAISS

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def build_user_faiss(username):

    processed_file = (
        f"../users/{username}/processed_data/"
        f"processed_user_data.json"
    )

    if not os.path.exists(processed_file):

        raise FileNotFoundError(
            f"Processed data not found: {processed_file}"
        )

    with open(
        processed_file,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    docs = []

    for item in data:

        text = item.get("text", "").strip()

        if not text:
            continue

        docs.append(

            Document(

                page_content=text,

                metadata={

                    "source": item.get(
                        "source",
                        "unknown"
                    ),

                    "type": item.get(
                        "type",
                        "unknown"
                    )
                }
            )
        )

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100
    ).split_documents(docs)

    faiss_path = (
        f"../users/{username}/faiss_index"
    )

    os.makedirs(
        faiss_path,
        exist_ok=True
    )

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    vector_store.save_local(faiss_path)

    return True
