import os
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from config import OUTPUT_KB_CHROMA
from knowledge_base.vector_db.db_utils import add_document, update_document, read_document, remove_document
from utils.wrapper import EmbeddingWrapper

wrapper = EmbeddingWrapper()

vector_store = Chroma(
    collection_name="files",
    embedding_function=wrapper.embedding,
    persist_directory=OUTPUT_KB_CHROMA,
    collection_metadata={
        "hnsw:space": "cosine"
    }
)


def reset_file(file_path: str):
    filename = os.path.basename(file_path)
    document = read_document(filename)

    if document:
        # a previous version of file is uploaded
        # clear vector db
        ids = []
        for index in range(0, document['chunks']):
            ids.append(f"{filename}_{index}")

        vector_store.delete(ids=ids)
        # clear db
        update_document(filename=filename, chunks=0)

    return document


def load_document(file_path, document):
    filename = os.path.basename(file_path)
    chunks, ids = [], []

    if filename.endswith(".pdf"):
      document_loader = PyPDFLoader(file_path)
      # Load PDF documents and return them as a list of Document objects
      documents = document_loader.load()

      splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,  # Size of each chunk in characters
        chunk_overlap=100,  # Overlap between consecutive chunks
        length_function=len,  # Function to compute the length of the text
        add_start_index=True,  # Flag to add start index to each chunk
      )
      chunks = splitter.split_documents(documents)
    elif filename.endswith(".md"):
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
        if filename == 'Codice Galattico.md':
            headers_to_split_on.extend([("####", "Header 4")])
        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

        with open(file_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()
            chunks = splitter.split_text(markdown_content)



    if not document:
        add_document(filename, len(chunks))
    else:
        update_document(filename, len(chunks))

    for index, chunk in enumerate(chunks):
        # metadata = {'type': random.choice(['Paris', 'London', 'Milan'])}
        #chunk.metadata = metadata
        ids.append(f"{filename}_{index}")

    return chunks, ids


def save_to_chroma(chunks: list[Document], ids : list[int]):
    vector_store.add_documents(documents=chunks, ids=ids)


def delete_document(file_path: str):
    filename = os.path.basename(file_path)

    document = read_document(filename)
    if document:
        ids = []
        for index in range(0, document['chunks']):
            ids.append(f"{filename}_{index}")
        vector_store.delete(ids=ids)
        remove_document(filename)


def loader(file_path: str, operation: str = 'add'):
    if operation == 'add':
        document = reset_file(file_path)    # clean previous chunks through ids
        chunks, ids = load_document(file_path, document)    # split new document in chunks
        save_to_chroma(chunks, ids)
    elif operation == 'delete':
        delete_document(file_path)


def search(query: str, k: int = 4, filter: dict = None, score: bool = False):
    if score:
        return vector_store.similarity_search_with_score(query, k, filter)
    else:
        return vector_store.similarity_search(query, k, filter)