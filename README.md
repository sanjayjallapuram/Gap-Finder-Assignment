GapFinder AI
An AI-powered study assistant that uses Retrieval-Augmented Generation
(RAG) to analyse a student's study materials, generate source-grounded
questions, identify learning gaps, and create a personalised revision
plan.
Features
- PDF ingestion: Load PDF study materials and extract page-level
  text.
- Document classification: Classify files as syllabus material,
  past papers, or general study material using filename-based rules.
- Text chunking: Split extracted text into overlapping chunks for
  retrieval.
- Vector search: Generate embeddings with Hugging Face Sentence
  Transformers and store document chunks in ChromaDB.
- Topic mapping: Use the Groq API to identify topics, subtopics,
  and estimated exam importance from the available materials.
- RAG-based question generation: Generate multiple-choice
  questions using retrieved document context, with source filename and
  page references.
- Diagnostic assessment: Evaluate answers and calculate
  topic-level scores.
- Learning-gap analysis: Classify topics as weak, medium, or
  strong and prioritise revision.
- Revision planning: Allocate available study time across topics
  according to their calculated priority.
- Learning progress: Store quiz-attempt scores in SQLite.
The generated answers and questions are intended to be grounded in the
indexed study materials. Their accuracy still depends on the quality
of the source documents, retrieval, and model output.

How it works
1. Add or upload PDF study materials.
2. Extract text from each PDF and split it into chunks.
3. Create embeddings and index the chunks in ChromaDB.
4. Build a topic map from the indexed materials.
5. Retrieve relevant chunks when a topic needs to be explained or
   assessed.
6. Send the retrieved context to the Groq model to generate questions
   or explanations.
7. Record quiz results, analyse learning gaps, and produce a revision
   plan.
Technology stack
- Language: Python
- UI: Streamlit (for the web application interface)
- LLM API: Groq
- Orchestration and document processing: LangChain integrations
- PDF loader: PyPDFLoader
- Text splitting: RecursiveCharacterTextSplitter
- Embeddings: Hugging Face Sentence Transformers
  (sentence-transformers/all-MiniLM-L6-v2 by default)
- Vector database: ChromaDB
- Local progress database: SQLite
- Configuration: python-dotenv
Project structure
The project is organised by responsibility. Adjust the names below to
match the files in your repository.
GapFinder-AI/
├── app.py
├── ingestion_pipeline.py
├── config/
│   └── settings.py
├── services/
│   ├── llm_service.py
│   ├── document_service.py
│   ├── vector_store.py
│   ├── rag_service.py
│   ├── topic_service.py
│   └── question_service.py
├── modules/
│   ├── quiz.py
│   ├── gap_analysis.py
│   ├── revision_planner.py
│   └── progress.py
├── database/
│   └── db_manager.py
├── data/
│   ├── uploads/
│   ├── chroma_db/
│   ├── topics.json
│   └── latest_report.json
├── requirements.txt
├── .env.example
└── .gitignore
Some folders and files may be created automatically when the application
runs. Keep generated data and source code separate.
Prerequisites
- Python 3.10 or a compatible version supported by your installed
  dependencies.
- A Groq API key.
- Git, if you plan to clone or push the project through GitHub.
Local setup
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
Or open the project directory you already have.
2. Create and activate a virtual environment
Windows PowerShell:
python -m venv .venv
.venv\Scripts\Activate.ps1
macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
If you have not created requirements.txt yet, the following are the
main packages imported by the original implementation. Check your
current code and pin compatible versions before deployment:
pip install streamlit python-dotenv groq langchain-community langchain-text-splitters langchain-chroma langchain-huggingface sentence-transformers pypdf
4. Configure environment variables
Create a .env file in the project root:
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
Use a valid model identifier available to your Groq account. Do not
commit .env or expose API keys in source code.

An optional .env.example can contain the variable names with
placeholder values, but never a real key.
5. Add study materials
Place PDF files in the configured upload directory (the original
implementation uses data/uploads/) or upload them through the
application's interface.

For best results, use text-based PDFs. Scanned PDFs may require OCR,
which is not implemented in the original PDF-loading flow.
6. Run the application
For a Streamlit application:
streamlit run app.py
If you are running the original command-line version instead of the
Streamlit interface, run the module that contains its command-line entry
point.
Deploying to Streamlit Community Cloud
1. Push the project to a GitHub repository.
2. Open Streamlit Community Cloud.
3. Create an app and select the repository, branch, and app.py as the
   main file.
4. Open the app's settings and add the required secrets in TOML format:
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "openai/gpt-oss-120b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
5. Save the secrets and deploy the application.
The application must read the key from st.secrets in Streamlit Cloud
and may read from .env during local development.
Deployment and persistence notes
- Never push .env, API keys, tokens, or secrets.toml to GitHub.
- Add .env, .venv/, __pycache__/, and generated local data to
  .gitignore as appropriate.
- Streamlit Community Cloud's local filesystem should not be treated
  as durable storage. Uploaded PDFs, ChromaDB files, SQLite databases,
  and generated JSON files may not survive app restarts or
  redeployments.
- For a production deployment where user data must persist, use
  durable external storage and a persistent database/vector database.
  Consider user isolation and access controls if multiple students use
  the application.
- The Hugging Face embedding model may need to download during
  startup, which can increase initial load time.
Security
- Store secrets in environment variables locally and Streamlit Secrets
  in the cloud.
- Rotate any API key that has accidentally been committed or exposed.
- Do not commit student data or private study documents unless you
  have permission to share them.
- Validate uploaded file types and sizes before processing.
Current limitations and considerations
- Document classification in the original implementation is based on
  filename keywords.
- The original implementation expects text to be extractable from
  PDFs; image-only scans need OCR support.
- Generated questions depend on retrieved context and LLM output, so
  they should be reviewed before high-stakes use.
- SQLite and local ChromaDB are suitable for a local prototype, but
  multi-user production deployment requires a persistent storage
  strategy.
- The original code's terminal-based input() and print()
  interactions need to be replaced with Streamlit widgets for a fully
  interactive Streamlit experience.
Future improvements
- Add OCR for scanned PDFs.
- Add user authentication and per-user document isolation.
- Add durable cloud storage for uploaded files and vector indexes.
- Add automated tests for ingestion, retrieval, question generation,
  scoring, and revision planning.
- Add support for exporting diagnostic reports and revision schedules.
- Add document-level filtering and stronger citation validation.
License
Add a license file if you intend to distribute or open-source this
project. Until then, no license is specified.
