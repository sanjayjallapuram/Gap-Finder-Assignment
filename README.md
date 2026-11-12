# GapFinder AI – AI-Powered Student Knowledge Gap Detection System

## Project Overview

GapFinder AI is an AI-powered educational assistant designed to identify students' knowledge gaps, evaluate their understanding, and generate personalized study plans.

It uses **Retrieval-Augmented Generation (RAG)** to analyse uploaded study materials, extract important topics, generate context-based multiple-choice questions, and evaluate student performance.

The system helps students understand which topics they need to improve and prioritizes their preparation based on performance and exam importance.

## Key Features

- **PDF Document Ingestion:** Upload and process study materials, syllabi, and previous question papers.
- **Document Classification:** Identify syllabus documents, past examination papers, and study materials.
- **Text Chunking:** Split documents into smaller overlapping chunks for effective retrieval.
- **Vector Database:** Store document embeddings using ChromaDB.
- **Topic Extraction:** Automatically identify important topics and subtopics using an LLM.
- **AI Question Generation:** Generate multiple-choice questions based on retrieved study materials.
- **Diagnostic Quiz:** Evaluate student knowledge through topic-based assessments.
- **Knowledge Gap Analysis:** Identify weak, medium, and strong topics based on quiz performance.
- **Exam Priority Analysis:** Prioritize topics using performance scores and estimated exam importance.
- **Personalized Revision Planner:** Generate study schedules based on available days, study hours, and topic priorities.
- **RAG-Based Topic Explanation:** Provide explanations grounded in uploaded study materials.
- **Learning Progress Tracking:** Store and monitor quiz performance using SQLite.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| LLM | Groq API |
| LLM Integration | Groq Python SDK |
| RAG Framework | LangChain |
| PDF Processing | PyPDFLoader |
| Text Splitting | RecursiveCharacterTextSplitter |
| Embeddings | Hugging Face Sentence Transformers |
| Vector Database | ChromaDB |
| Database | SQLite |
| Data Processing | JSON |
| Environment Management | Python-dotenv |
| Deployment | Streamlit Community Cloud |

## 🧠 System Architecture

The application follows a Retrieval-Augmented Generation architecture.

1. **Document Upload:** Students upload PDFs containing study materials, syllabi, and previous examination papers.
2. **Document Processing:** PyPDFLoader extracts text from PDF documents.
3. **Text Chunking:** RecursiveCharacterTextSplitter divides extracted text into overlapping chunks.
4. **Embedding Generation:** Hugging Face embedding models convert text chunks into vector representations.
5. **Vector Storage:** ChromaDB stores embeddings and associated document metadata.
6. **Topic Mapping:** Groq LLM analyses study materials and extracts important topics and subtopics.
7. **Context Retrieval:** The retriever uses Maximal Marginal Relevance (MMR) to retrieve relevant document chunks.
8. **Question Generation:** Groq generates multiple-choice questions using retrieved context.
9. **Performance Evaluation:** Student responses are evaluated to calculate topic-level scores.
10. **Gap Analysis:** The system identifies knowledge gaps and calculates topic priorities.
11. **Revision Planning:** A personalized study schedule is generated based on learning gaps and available study time.

## 📂 Project Structure

```text
GapFinder-AI/
│
├── app.py
├── gapfinder.py        # just for reviewing the whole code at once(all the functions at one place)
│
├── services/
│   ├── llm_service.py
│   ├── document_service.py
│   ├── question_service.py
│   ├── rag_service.py
│   ├── topic_service.py
│   ├── vector_store.py
│   └── ingestion_pipeline.py

│
├── modules/
│   ├── quiz.py
│   ├── gap_analysis.py
│   ├── progress.py
│   └── revision_planner.py
│
├── database/
│   └── db_manager.py
│
└── data/
    ├── uploads/
    ├── chroma_db/
    ├── topics.json
    └── latest_report.json
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sanjayjallapuram/Gap-Finder-Assignment
```

```bash
cd YOUR_REPOSITORY
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

Replace the placeholder with your actual Groq API key.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| GROQ_API_KEY | API key for accessing Groq LLM services |
| GROQ_MODEL | Groq model used for text generation |
| EMBEDDING_MODEL | Hugging Face embedding model used for vector generation |

## ☁️ Deployment

The application can be deployed using **Streamlit Community Cloud**.

1. Push the project to a GitHub repository.
2. Visit https://share.streamlit.io/
3. Connect your GitHub account.
4. Select the project repository.
5. Select the `main` branch.
6. Set `app.py` as the main application file.
7. Configure the required API keys under Streamlit Cloud Secrets.
8. Deploy the application.

Example Streamlit Secrets configuration:

```toml
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "openai/gpt-oss-120b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

## 📊 Knowledge Gap Analysis

The system classifies student performance into three categories:

| Performance Score | Classification |
|---|---|
| Below 50% | Weak |
| 50% – 74.99% | Medium |
| 75% and above | Strong |

Topic priority is calculated using:

```text
Priority = 0.7 × (100 - Score)
         + 0.3 × (Exam Weight × 20)
```

Topics with higher priority receive more revision time.


live link: https://sanjayjallapuram-gapfinder-app-x0e7gf.streamlit.app/
