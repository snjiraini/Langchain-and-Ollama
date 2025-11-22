# Legal RAG Pipeline V4 Complete 🏛️⚖️

A production-ready Retrieval-Augmented Generation (RAG) system for legal document question answering, built with advanced chunking strategies, semantic search, and specialized legal prompts.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL 18+](https://img.shields.io/badge/PostgreSQL-18+-blue.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Pipeline Stages](#pipeline-stages)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Performance Metrics](#performance-metrics)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This notebook implements a complete end-to-end RAG pipeline specifically designed for legal documents. It processes PDF documents through multiple stages including OCR, semantic chunking, embedding generation, deduplication, and intelligent retrieval with customizable prompts.

### Key Highlights

- **814 embedded chunks** with 98% success rate (814/831 chunks)
- **4 specialized prompts** for different legal query types
- **Advanced retrieval** with similarity search and MMR (Maximal Marginal Relevance)
- **Production-ready** with comprehensive QA checks and error handling
- **Metadata filtering** by document version and section
- **7/7 QA checks passed** ensuring pipeline quality

## ✨ Features

### Document Processing

- 📄 **PDF Extraction**: Multi-engine support (PyMuPDF, pdfplumber, EasyOCR)
- 🔍 **OCR Integration**: Automatic detection of scanned documents
- 🧹 **Text Cleaning**: Removes headers, footers, page numbers, and formatting artifacts
- 📊 **Metadata Extraction**: Document title, jurisdiction, dates, sections

### Advanced Chunking

- 🎯 **Semantic Chunking**: Context-aware splitting at natural boundaries
- 📏 **Token-Aware**: Respects token limits (350 tokens max including metadata)
- 🏗️ **Hierarchy-Aware**: Preserves document structure (chapters, sections)
- 🔄 **Overlap Strategy**: Configurable overlap for context continuity

### Embedding & Storage

- 🧮 **768-dimensional embeddings** using Ollama's nomic-embed-text
- 🐘 **PostgreSQL + pgvector**: High-performance vector storage
- 🔢 **Batch Processing**: Efficient embedding generation with progress tracking
- 💾 **Persistent Storage**: All data stored in PostgreSQL with versioning

### Intelligent Retrieval

- 🔎 **Similarity Search**: Cosine distance-based retrieval
- 🎲 **MMR Support**: Diverse results to avoid redundancy
- 🏷️ **Metadata Filtering**: Filter by document version, section, or custom fields
- ⚙️ **Configurable Parameters**: Adjust k, score threshold, and diversity

### Quality Assurance

- ✅ **7 Comprehensive QA Checks**:
  1. Document metadata validation
  2. OCR quality verification
  3. Chunk coverage analysis
  4. Embedding dimension verification
  5. Token count compliance
  6. Duplicate detection
  7. Retrieval system testing

### RAG System

- 🤖 **LLM Integration**: Ollama with llama3.2:3b model
- 📝 **4 Specialized Prompts**:
  - **General QA**: Accessible legal information
  - **Citation**: Detailed citations and quotes
  - **Comparison**: Cross-document analysis
  - **Summary**: Concise topical summaries
- 🔧 **Helper Functions**: Production-ready wrapper functions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Legal Documents (PDF)                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  PDF Extraction  │
                    │  & OCR (EasyOCR) │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Text Cleaning &  │
                    │    Metadata      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Semantic        │
                    │  Chunking        │
                    │  (814 chunks)    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Embeddings      │
                    │  (nomic-embed)   │
                    │  768 dimensions  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  PostgreSQL      │
                    │  + pgvector      │
                    │  Storage         │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────┐      ┌──────▼──────┐     ┌─────▼─────┐
    │Similarity│      │   MMR       │     │ Metadata  │
    │  Search  │      │ Diversity   │     │ Filtering │
    └────┬────┘      └──────┬──────┘     └─────┬─────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────▼────────┐
                    │  LLM Integration │
                    │  (llama3.2:3b)   │
                    │  + Prompts       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Question        │
                    │  Answering       │
                    │  System          │
                    └──────────────────┘
```

## 🔧 Prerequisites

### System Requirements

- **Python**: 3.11 or higher
- **PostgreSQL**: 18.0 or higher
- **Ollama**: Latest version
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 5GB for models and data

### Software Dependencies

- PostgreSQL with pgvector extension
- Ollama with required models:
  - `nomic-embed-text` (embeddings)
  - `llama3.2:3b` (LLM)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/snjiraini/Langchain-and-Ollama.git
cd "Langchain-and-Ollama/17.2 RAG-V4 Improved"
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install PostgreSQL and pgvector

**macOS (using Homebrew):**

```bash
brew install postgresql@18
brew services start postgresql@18

# Install pgvector
cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
make install  # May require sudo
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install postgresql-18 postgresql-contrib-18
sudo systemctl start postgresql

# Install pgvector
sudo apt install postgresql-18-pgvector
```

### 5. Install Ollama and Models

**macOS/Linux:**

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

### 6. Setup Database

```bash
# Initialize database
python init_db.py

# Verify setup
python verify_setup.py
```

### 7. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
nano .env
```

## 🚀 Quick Start

### 1. Start Services

```bash
# Start PostgreSQL (if not running)
brew services start postgresql@18  # macOS
# or
sudo systemctl start postgresql     # Linux

# Start Ollama (if not running)
ollama serve
```

### 2. Open the Notebook

```bash
jupyter lab Legal_RAG_Pipeline_V4_Complete.ipynb
```

### 3. Run All Cells

Execute the notebook cells in order. The pipeline will:

1. **Load Configuration** (Cells 1-4)
2. **Process Documents** (Cells 5-20)
3. **Generate Chunks** (Cells 21-50)
4. **Create Embeddings** (Cells 51-70)
5. **Setup Versioning** (Cells 71-75)
6. **Run QA Checks** (Cells 76-89)
7. **Initialize RAG System** (Cells 90-111)
8. **Test the System** (Cells 112-114)

### 4. Query the System

```python
# Simple question answering
result = rag_chain.query("What are the fundamental rights guaranteed?")
print(result['answer'])

# With advanced options
result = rag_chain.query(
    question="citizenship requirements",
    prompt_type='citation',  # Get detailed citations
    k=5,                     # Retrieve 5 sources
    use_mmr=True,           # Use diverse results
    filter_version_id="v_a7cab3e9dbb6"  # Filter by document
)

print(f"Answer: {result['answer']}")
print(f"Sources: {result['num_sources']}")
```

## 📊 Pipeline Stages

### Stage 1: Document Ingestion (Cells 1-20)

- PDF extraction and OCR
- Text cleaning and preprocessing
- Metadata extraction
- Document classification

**Key Outputs:**

- Extracted text files
- Metadata JSON files
- Classification results
- OCR confidence scores

### Stage 2: Semantic Chunking (Cells 21-50)

- Hierarchy-aware splitting
- Section boundary detection
- Token-aware re-chunking
- Metadata overhead accounting

**Key Outputs:**

- 831 initial chunks
- 814 final chunks (98% success rate)
- Average chunk size: ~200-300 tokens
- All chunks compliant with 350 token limit

### Stage 3: Embedding Generation (Cells 51-70)

- Batch processing with progress tracking
- Error handling and retry logic
- Vector storage in PostgreSQL
- Dimension verification

**Key Outputs:**

- 814 embeddings (768-dimensional)
- 98% completion rate
- Average embedding time: ~0.5s per chunk

### Stage 4: Versioning & Deduplication (Cells 71-75)

- Shingle hashing for duplicate detection
- Cross-document duplicate analysis
- Version tracking and management
- Superseded document handling

**Key Outputs:**

- Duplicate groups identified
- Version relationships established
- Amendment tracking enabled

### Stage 5: Quality Assurance (Cells 76-89)

- 7 comprehensive QA checks
- Validation of all pipeline stages
- Performance metrics collection
- Error identification and reporting

**Key Outputs:**

- 7/7 checks passed ✅
- Pipeline validated for production
- Performance benchmarks established

### Stage 6: RAG System Setup (Cells 90-114)

- PGVector store initialization
- Custom retriever implementation
- Specialized prompt creation
- LLM integration
- End-to-end testing

**Key Outputs:**

- Production-ready RAG system
- 4 specialized prompts
- Helper functions for easy integration
- Complete documentation

## ⚙️ Configuration

### Database Configuration (.env)

```bash
# PostgreSQL Database
DB_NAME=legalrag_v4_db        # Database name
DB_USER=quest                  # Your username
DB_HOST=localhost             # Database host
DB_PORT=5432                  # Database port
DB_PASSWORD=quest             # Database password (optional for local)
```

### Ollama Configuration (.env)

```bash
# Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBED_MODEL=nomic-embed-text    # Embedding model
OLLAMA_LLM_MODEL=llama3.2:3b          # Language model
```

### Chunking Parameters (Notebook Cell 3)

```python
CHUNK_CONFIG = {
    'target_chunk_size': 300,      # Target tokens per chunk
    'max_chunk_size': 350,         # Maximum tokens (hard limit)
    'overlap_percentage': 0.15,    # 15% overlap between chunks
    'overlap_tokens': 45,          # ~15% of 300
    'metadata_overhead': 50,       # Estimated metadata tokens
}
```

### Embedding Configuration (Notebook Cell 3)

```python
EMBEDDING_CONFIG = {
    'model': 'nomic-embed-text',   # Ollama embedding model
    'dimensions': 768,             # Embedding dimensions
    'batch_size': 10,              # Chunks per batch
    'delay_between_batches': 1.0,  # Seconds between batches
    'max_retries': 3,              # Retry attempts on failure
}
```

### RAG Configuration (Notebook Cell 3)

```python
RAG_CONFIG = {
    'llm_model': 'llama3.2:3b',    # Ollama LLM model
    'temperature': 0.1,             # Low for factual responses
    'context_window': 4096,         # Token context window
    'default_k': 5,                 # Default retrieval count
    'score_threshold': 0.3,         # Minimum similarity score
    'use_mmr': True,                # Enable MMR by default
}
```

## 💡 Usage Examples

### Basic Question Answering

```python
# Ask a question
result = rag_chain.query("What are citizenship requirements?")
print(result['answer'])
```

### Citation-Focused Query

```python
# Get detailed citations
result = rag_chain.query(
    question="What are voting procedures?",
    prompt_type='citation'
)

print(result['answer'])
for i, source in enumerate(result['sources'], 1):
    print(f"\nSource {i}:")
    print(f"  Document: {source['metadata']['document']}")
    print(f"  Section: {source['metadata'].get('section_ref', 'N/A')}")
    print(f"  Similarity: {source['metadata']['similarity']:.3f}")
```

### Cross-Document Comparison

```python
# Compare across multiple documents
result = rag_chain.query(
    question="How do election procedures differ?",
    prompt_type='comparison',
    k=10
)
print(result['answer'])
```

### Filtered Search

```python
# Search specific document version
result = rag_chain.query(
    question="government structure",
    filter_version_id="v_a7cab3e9dbb6",
    k=5
)

# Search specific section
result = rag_chain.query(
    question="fundamental rights",
    filter_section="Chapter",
    k=5
)
```

### Direct Retrieval (No LLM)

```python
# Get raw chunks without LLM generation
docs = retriever.retrieve(
    query="citizenship",
    k=10,
    use_mmr=True
)

for doc in docs:
    print(f"Similarity: {doc.metadata['similarity']:.3f}")
    print(f"Content: {doc.page_content[:200]}...")
    print()
```

### Helper Functions

```python
# Use production helper functions
from helper_functions import (
    ask_legal_question,
    search_legal_documents,
    compare_documents
)

# Simple QA
result = ask_legal_question("What are fundamental rights?")

# Search without LLM
results = search_legal_documents("voting rights", k=10)

# Compare documents
comparison = compare_documents(
    query="elections",
    version_ids=['v1', 'v2']
)
```

## 📈 Performance Metrics

### Pipeline Statistics

| Metric               | Value         |
| -------------------- | ------------- |
| Total Documents      | 4             |
| Total Chunks         | 814           |
| Success Rate         | 98% (814/831) |
| Embedding Dimensions | 768           |
| Average Chunk Tokens | ~250          |
| Database Size        | ~500 MB       |

### Processing Times

| Stage                | Average Time             |
| -------------------- | ------------------------ |
| PDF Extraction       | ~2-5 seconds/page        |
| Text Cleaning        | ~1 second/document       |
| Semantic Chunking    | ~5-10 seconds/document   |
| Embedding Generation | ~0.5 seconds/chunk       |
| Total Pipeline       | ~5-10 minutes for 4 docs |

### Query Performance

| Operation         | Average Time  |
| ----------------- | ------------- |
| Similarity Search | ~50-100 ms    |
| MMR Retrieval     | ~100-200 ms   |
| LLM Response      | ~8-10 seconds |
| End-to-End Query  | ~8-12 seconds |

### Quality Metrics

| Check               | Status  | Details                    |
| ------------------- | ------- | -------------------------- |
| Document Validation | ✅ PASS | 4/4 documents valid        |
| OCR Quality         | ✅ PASS | Validated in preprocessing |
| Chunk Coverage      | ✅ PASS | 814 chunks, 4 documents    |
| Embeddings          | ✅ PASS | 814/814 (100%), 768-dim    |
| Token Compliance    | ✅ PASS | Excellent compliance       |
| Duplicates          | ✅ PASS | Groups identified          |
| Retrieval           | ✅ PASS | All queries successful     |

## 📁 Project Structure

```
17.2 RAG-V4 Improved/
├── Legal_RAG_Pipeline_V4_Complete.ipynb  # Main notebook
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
├── .env.example                          # Environment template
├── .env                                  # Your configuration (gitignored)
├── init_db.py                            # Database initialization
├── verify_setup.py                       # Setup verification
│
├── legal_documents/                      # PDF documents
│   ├── TheConstitutionOfKenya.pdf
│   ├── Acts Published for the Implementation...pdf
│   └── ...
│
├── pipeline_storage/                     # Processing outputs
│   ├── extracted/                        # Raw text from PDFs
│   ├── cleaned/                          # Cleaned text
│   ├── metadata/                         # Document metadata
│   ├── structure/                        # Document structure
│   ├── classification/                   # Page classifications
│   ├── chunks/                           # Generated chunks
│   └── embeddings/                       # Embedding data
│
├── rag-dataset/                          # Additional datasets
│   └── kenya_constitution/
│
└── docs/                                 # Additional documentation
    ├── ARCHITECTURE.md
    ├── API.md
    └── DEPLOYMENT.md
```

## 🔍 Troubleshooting

### Common Issues

#### 1. PostgreSQL Connection Error

**Problem:** `psycopg2.OperationalError: could not connect to server`

**Solution:**

```bash
# Check if PostgreSQL is running
brew services list  # macOS
sudo systemctl status postgresql  # Linux

# Start if not running
brew services start postgresql@18  # macOS
sudo systemctl start postgresql    # Linux

# Verify connection
psql -U quest -d legalrag_v4_db
```

#### 2. pgvector Extension Not Found

**Problem:** `ERROR: could not open extension control file`

**Solution:**

```bash
# Reinstall pgvector
cd /tmp
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make clean
make
sudo make install

# Restart PostgreSQL
brew services restart postgresql@18
```

#### 3. Ollama Model Not Found

**Problem:** `ResponseError: model 'llama3.2:3b' not found`

**Solution:**

```bash
# Check available models
ollama list

# Pull missing models
ollama pull nomic-embed-text
ollama pull llama3.2:3b

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

#### 4. Memory Error During Embedding

**Problem:** `MemoryError` or slow embedding generation

**Solution:**

```python
# Reduce batch size in notebook cell
EMBEDDING_CONFIG = {
    'batch_size': 5,  # Reduced from 10
    'delay_between_batches': 2.0,  # Increased delay
}
```

#### 5. Transaction Errors

**Problem:** `InFailedSqlTransaction` errors

**Solution:**

```python
# Run rollback in notebook cell
conn.rollback()
print("✅ Transaction rolled back")
```

#### 6. Slow Query Performance

**Problem:** Retrieval queries taking too long

**Solution:**

```sql
-- Create index if missing (run in psql)
CREATE INDEX IF NOT EXISTS idx_embeddings_vector
ON embeddings USING ivfflat (embedding_vector vector_cosine_ops);

-- Vacuum analyze
VACUUM ANALYZE embeddings;
```

### Getting Help

If you encounter issues not covered here:

1. **Check the Logs**: Look for error messages in notebook output
2. **Verify Setup**: Run `python verify_setup.py`
3. **Check Versions**: Ensure all dependencies match requirements
4. **Database State**: Query database to check data integrity
5. **Open an Issue**: Create a GitHub issue with:
   - Error message
   - System info (OS, Python version, etc.)
   - Steps to reproduce

## 🚀 Deployment

### Production Deployment Options

#### 1. FastAPI Application

```python
# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Legal RAG API")

class Query(BaseModel):
    question: str
    prompt_type: str = "qa"
    k: int = 5

@app.post("/query")
async def query_rag(query: Query):
    result = rag_chain.query(
        question=query.question,
        prompt_type=query.prompt_type,
        k=query.k
    )
    return result
```

#### 2. Streamlit Application

```python
# streamlit_app.py
import streamlit as st

st.title("Legal Document Q&A")

question = st.text_input("Ask a legal question:")
if st.button("Search"):
    with st.spinner("Searching..."):
        result = rag_chain.query(question)
        st.write(result['answer'])

        with st.expander("View Sources"):
            for source in result['sources']:
                st.write(source)
```

#### 3. Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### Scaling Considerations

- **Database**: Use connection pooling for multiple workers
- **Caching**: Implement Redis for common queries
- **Load Balancing**: Use Nginx or similar for distribution
- **Monitoring**: Add logging and metrics (Prometheus, Grafana)

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the Repository**
2. **Create a Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Commit Changes**: `git commit -m 'Add amazing feature'`
4. **Push to Branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Setup

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black .
isort .

# Type checking
mypy .
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain**: For the RAG framework
- **Ollama**: For local LLM and embedding models
- **pgvector**: For efficient vector storage
- **PostgreSQL**: For robust database management
- **PyMuPDF**: For PDF processing
- **EasyOCR**: For optical character recognition

## 📧 Contact

- **Author**: Samuel Njiraini
- **Repository**: [Langchain-and-Ollama](https://github.com/snjiraini/Langchain-and-Ollama)
- **Issues**: [GitHub Issues](https://github.com/snjiraini/Langchain-and-Ollama/issues)

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Hybrid search (keyword + semantic)
- [ ] Conversation memory
- [ ] Document summarization
- [ ] Web UI (Streamlit/Gradio)
- [ ] REST API (FastAPI)
- [ ] User authentication
- [ ] Query caching
- [ ] Admin dashboard
- [ ] A/B testing framework
- [ ] Model fine-tuning
- [ ] Custom embedding models
- [ ] Real-time document updates
- [ ] Export functionality
- [ ] Analytics and reporting

---

**Built with ❤️ for legal professionals and researchers**

_Last Updated: November 22, 2025_
