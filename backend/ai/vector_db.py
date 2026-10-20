
import os
import re
import shutil

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ai.embeddings import get_embeddings


VECTOR_DB_PATH = "./vectorstore"
KNOWLEDGE_PATH = "./knowledge/plant_care.txt"


def create_vector_db(rebuild=False):
    if rebuild and os.path.exists(VECTOR_DB_PATH):
        shutil.rmtree(VECTOR_DB_PATH)

    loader = TextLoader(
        KNOWLEDGE_PATH,
        encoding="utf-8"
    )
    documents = loader.load()
    text = documents[0].page_content

    sections = re.split(
        r"(?m)(?=^[A-Z][A-Z ]{2,}$)",
        text
    )

    section_documents = [
        Document(
            page_content=section.strip(),
            metadata=documents[0].metadata
        )
        for section in sections
        if section.strip()
    ]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(section_documents)

    embeddings = get_embeddings()

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    print(f"Created vector database with {len(chunks)} chunks.")
    return vector_db


def get_vector_db():
    embeddings = get_embeddings()

    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )
