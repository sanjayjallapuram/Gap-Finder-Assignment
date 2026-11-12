from config.settings import vector_store
from services.vector_store import get_retriever
# =========================================================
# 6. RAG RETRIEVAL
# =========================================================

def retrieve_context(query, top_k=5):
    """
    Retrieve relevant Document chunks through LangChain's MMR retriever.
    """
    active_retriever = get_retriever()

    # Allow callers to request a different number of chunks.
    if top_k != 5:
        active_retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": top_k,
                "fetch_k": max(top_k * 3, 10),
                "lambda_mult": 0.7
            }
        )

    documents = active_retriever.invoke(query)
    retrieved = []

    for index, document in enumerate(documents):
        metadata = document.metadata
        retrieved.append({
            "id": f"S{index + 1}",
            "text": document.page_content,
            "source": metadata.get("source", "Unknown source"),
            "page": metadata.get(
                "page_number",
                int(metadata.get("page", 0)) + 1
            )
        })

    return retrieved


def format_context(documents):
    context = ""

    for doc in documents:
        context += (
            f"\n[SOURCE_ID: {doc['id']}]\n"
            f"File: {doc['source']}\n"
            f"Page: {doc['page']}\n"
            f"Content: {doc['text']}\n"
        )

    return context
