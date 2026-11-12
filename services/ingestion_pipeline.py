from config.settings import UPLOAD_DIR,CHROMA_DIR,TOPICS_PATH,REPORT_PATH,Path,embeddings
from services.document_service import process_documents
from services.vector_store import create_vector_store
from services.topic_service import build_topic_map
from langchain_chroma import Chroma


# =========================================================
# 13. DOCUMENT INGESTION PIPELINE
# =========================================================

def ingest_documents():

    chunks = process_documents(UPLOAD_DIR)

    if not chunks:
        raise ValueError(
            "No readable text found in uploaded PDFs."
        )

    create_vector_store(chunks)

    build_topic_map(chunks)

    print("\nDocument ingestion completed!")


def _delete_vector_collection():
    """Delete the persistent GapFinder collection and clear cached handles."""
    global vector_store, retriever

    try:
        store = Chroma(
            collection_name="gapfinder",
            embedding_function=embeddings,
            persist_directory=str(CHROMA_DIR)
        )
        store.delete_collection()
    except Exception:
        # The collection may not exist yet. The on-disk directory is handled
        # by Chroma; do not delete it while a collection may be open.
        pass

    vector_store = None
    retriever = None


def _remove_derived_knowledge_files():
    """Remove topic mapping and latest diagnosis tied to the old documents."""
    for path in (TOPICS_PATH, REPORT_PATH):
        if path.exists():
            path.unlink()


def clear_uploaded_documents():
    """Remove every uploaded PDF and all derived RAG/topic/report data.

    Quiz-attempt history in SQLite is intentionally preserved.
    """
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    for pdf_file in UPLOAD_DIR.glob("*.pdf"):
        pdf_file.unlink()

    _delete_vector_collection()
    _remove_derived_knowledge_files()


def remove_document(filename):
    """Remove one PDF, then rebuild the index and topic map from remaining PDFs."""
    safe_name = Path(filename).name
    if safe_name != filename or not safe_name.lower().endswith(".pdf"):
        raise ValueError("Invalid PDF filename.")

    target = UPLOAD_DIR / safe_name
    if not target.is_file():
        raise FileNotFoundError(f"Document not found: {safe_name}")

    target.unlink()
    remaining = list(UPLOAD_DIR.glob("*.pdf"))

    if remaining:
        # ingest_documents recreates the Chroma collection from only the
        # remaining files and regenerates the topic map.
        ingest_documents()
    else:
        _delete_vector_collection()
        _remove_derived_knowledge_files()

    return [path.name for path in sorted(UPLOAD_DIR.glob("*.pdf"))]
