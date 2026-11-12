from config.settings import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =========================================================
# 4. PDF PROCESSING
# =========================================================

def process_documents(folder):
    """
    Load PDFs page-by-page with PyPDFLoader, preserve source metadata,
    and split pages into overlapping chunks with RecursiveCharacterTextSplitter.
    """
    print("\nReading PDF documents with PyPDFLoader...")

    pdf_files = sorted(Path(folder).glob("*.pdf"))
    if not pdf_files:
        raise ValueError(f"No PDF files found in {folder}")

    loaded_documents = []

    for pdf_file in pdf_files:
        print(f"Loading: {pdf_file.name}")

        loader = PyPDFLoader(str(pdf_file))
        page_documents = loader.load()

        for document in page_documents:
            # PyPDFLoader stores page indexes starting at zero.
            zero_based_page = document.metadata.get("page", 0)

            document.metadata["source"] = pdf_file.name
            document.metadata["page_number"] = int(zero_based_page) + 1
            document.metadata["document_type"] = classify_document(
                pdf_file.name
            )
            loaded_documents.append(document)

    if not loaded_documents:
        raise ValueError(
            "No readable text found. The PDFs may be scanned/image-only."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = splitter.split_documents(loaded_documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index

    print(f"Pages loaded: {len(loaded_documents)}")
    print(f"Chunks created: {len(chunks)}")
    return chunks


def classify_document(filename):

    name = filename.lower()

    if "syllabus" in name:
        return "syllabus"

    if "paper" in name or "exam" in name or "question" in name:
        return "past_paper"

    return "study_material"
