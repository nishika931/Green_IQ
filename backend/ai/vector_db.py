from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ai.embeddings import get_embeddings


VECTOR_DB_PATH = "./vectorstore"


def create_vector_db():
    loader = TextLoader(
        "./knowledge/plant_care.txt",
        encoding="utf-8"
    )

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)

    embeddings = get_embeddings()

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    return vector_db


def get_vector_db():
    embeddings = get_embeddings()

    vector_db = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    return vector_db