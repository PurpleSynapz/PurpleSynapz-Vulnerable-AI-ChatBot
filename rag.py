from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from config import rag_base_url, emb_model_name, chroma_persist_directory, chunk_size, chunk_overlap

# get the running ollama instance to generate embeddings for the ChromaDB vector store
def _get_embedding():
    return OllamaEmbeddings(base_url=rag_base_url, model=emb_model_name)

# get the ChromaDB vector store instance with the Ollama embeddings function
def _get_db():
    return Chroma(
        persist_directory=chroma_persist_directory,embedding_function=_get_embedding(),
    )

# creating the chomadb.
def create_chromadb():
    """Initialise the persisted Chroma database without resetting uploaded data."""
    db = _get_db()
    return db

# list the sources of the stored chunks in ChromaDB by reading the metadata of all stored items
def list_chromadb_sources():
    db = _get_db()
    payload = db.get(include=["metadatas"])
    metadatas = payload.get("metadatas", []) if payload else []
    print(f"[RAG] Listing stored sources from {len(metadatas)} metadata records")

    sources = {}
    for metadata in metadatas:
        if not metadata:
            continue

        source = metadata.get("source")
        if not source:
            continue

        current_count = sources.get(source, 0)
        sources[source] = current_count + 1

    return [
        {"filename": filename, "chunks_stored": chunk_count}
        for filename, chunk_count in sorted(sources.items())
    ]

# search the chromadb for the best matchig chunks to the give query.
def search_chromadb(query):
    print(f"[RAG] Query: {query}")
    db = _get_db()
    results = db.similarity_search_with_score(query, k=3)
    filtered_documents = []
    print("[RAG] Results:")
    for document, score in results:
        source = document.metadata.get("source", "unknown")
        chunk_index = document.metadata.get("chunk_index", "?")
        preview = document.page_content[:120].replace("\n", "\\n")
        print(f"- source={source} chunk={chunk_index} score={score} preview={preview}")
        if source == "unknown":
            continue
        filtered_documents.append(document)

    print(f"[RAG] Filtered documents kept: {len(filtered_documents[:4])}")
    return filtered_documents[:4]

# helper function to split the uploaded text into chunks with some overlap,
def _chunk_text(content, chunk_size=chunk_size, chunk_overlap=chunk_overlap):
    chunks = []
    start = 0
    text_length = len(content)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = content[start:end]

        if end < text_length:
            last_break = max(chunk.rfind("\n\n"), chunk.rfind("\n"), chunk.rfind(". "))
            if last_break > chunk_size // 2:
                end = start + last_break + 1
                chunk = content[start:end]

        cleaned_chunk = chunk.strip()
        if cleaned_chunk:
            chunks.append(cleaned_chunk)

        if end >= text_length:
            break

        start = max(end - chunk_overlap, start + 1)

    return chunks

# add a given text to chromadb.
def add_text_to_chromadb(filename, content, chunk_size=chunk_size, chunk_overlap=chunk_overlap):
    print(f"[RAG] Uploading file: {filename}")
    cleaned_content = content.strip()
    if not cleaned_content:
        raise ValueError("Uploaded file is empty.")

    print(f"[RAG] Cleaned content chars: {len(cleaned_content)}")
    print(f"[RAG] Chunk settings: chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
    chunks = _chunk_text(cleaned_content, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    metadatas = []
    for index, _chunk in enumerate(chunks):
        metadatas.append(
            {
                "source": filename,
                "chunk_index": index,
            }
        )

    if not chunks:
        raise ValueError("No readable text was found in the uploaded file.")

    print(f"[RAG] Total chunks prepared: {len(chunks)}")
    for index, chunk in enumerate(chunks):
        preview = chunk[:800].replace("\n", "\\n")
        print(f"[RAG] Chunk {index}: chars={len(chunk)} preview={preview}")

    db = _get_db()

    # Replace older chunks for the same file so reuploads stay consistent.
    existing_items = db.get(where={"source": filename})
    existing_ids = existing_items.get("ids", []) if existing_items else []
    if existing_ids:
        print(f"[RAG] Removing existing chunks for {filename}: {existing_ids}")
        db.delete(ids=existing_ids)

    ids = [f"{filename}-{chunk_index}" for chunk_index in range(len(chunks))]
    print(f"[RAG] Adding chunk IDs: {ids}")
    db.add_texts(texts=chunks, metadatas=metadatas, ids=ids)
    print(f"[RAG] Stored {len(chunks)} chunks from {filename}")

    return len(chunks)
