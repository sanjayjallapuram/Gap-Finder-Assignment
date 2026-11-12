from langchain_chroma import Chroma
from config.settings import embeddings,CHROMA_DIR

# =========================================================
# 5. VECTOR DATABASE
# =========================================================

def create_vector_store(chunks):
    """
    Create a persistent LangChain Chroma vector store and index chunks.
    Replaces the existing collection so ingestion can be repeated cleanly.
    """
    global vector_store, retriever

    print("\nCreating Chroma vector store...")

    try:
        old_store = Chroma(
            collection_name="gapfinder",
            embedding_function=embeddings,
            persist_directory=str(CHROMA_DIR)
        )
        old_store.delete_collection()
    except Exception:
        pass

    vector_store = Chroma(
        collection_name="gapfinder",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR)
    )

    batch_size = 100
    for start_index in range(0, len(chunks), batch_size):
        batch = chunks[start_index:start_index + batch_size]
        ids = [
            f"gapfinder_chunk_{start_index + offset}"
            for offset in range(len(batch))
        ]
        vector_store.add_documents(documents=batch, ids=ids)

    # MMR improves result diversity by reducing near-duplicate chunks.
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 15,
            "lambda_mult": 0.7
        }
    )

    print(f"Vector store created. Indexed {len(chunks)} chunks.")


def get_retriever():
    """Load the persistent vector store and return its MMR retriever."""
    global vector_store, retriever

    if retriever is None:
        vector_store = Chroma(
            collection_name="gapfinder",
            embedding_function=embeddings,
            persist_directory=str(CHROMA_DIR)
        )

        if vector_store._collection.count() == 0:
            raise ValueError(
                "Vector database is empty. Process PDF materials first."
            )

        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 5,
                "fetch_k": 15,
                "lambda_mult": 0.7
            }
        )

    return retriever
