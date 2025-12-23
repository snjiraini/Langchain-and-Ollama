# Legal RAG Pipeline V5 - Batch Processing Architecture 🏛️⚖️

A production-ready, batch-based Retrieval-Augmented Generation (RAG) system for legal document processing. Features folder-driven document ingestion, atomic batch file operations, LegalBERT OCR correction, and transactional database operations.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL 18+](https://img.shields.io/badge/PostgreSQL-18+-blue.svg)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **⚠️ Architecture Change**: V5 introduces a batch-based processing workflow with atomic file operations, centralized database access, and folder-driven document ingestion. See [Architecture Changes](#v5-architecture-changes) for details.

## 📋 Table of Contents

- [Overview](#overview)
- [V5 Architecture Changes](#v5-architecture-changes)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Batch Processing Workflow](#batch-processing-workflow)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Migration from V4](#migration-from-v4)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Legal RAG Pipeline V5 implements a robust, batch-based document processing system specifically designed for legal documents. The pipeline processes PDF documents through distinct stages with atomic file operations, transactional database access, and comprehensive error handling.

### Key Highlights

- **🔄 Batch-Based Processing**: Folder-driven workflow with atomic JSONL + pickle batch files
- **🗄️ Centralized Database Access**: Transaction-managed PostgreSQL operations with connection pooling
- **✍️ LegalBERT OCR Correction**: 45-term legal dictionary + 11 OCR patterns with audit logging
- **🧪 Comprehensive Testing**: End-to-end integration tests with 98%+ success rate
- **⚙️ Environment-Based Configuration**: All settings managed via `.env` files
- **📦 Modular Architecture**: Separate modules for chunking, ingestion, and OCR correction
- **🔒 Transaction Safety**: Automatic rollback on failures, idempotent re-runs

### V5 Architecture Changes

**What's New in V5:**

1. **Folder-Driven Document Ingestion**

   - Documents placed in `SOURCE_DIR` are automatically discovered
   - Processing occurs independently of database state
   - Source files archived after successful processing

2. **Batch File Operations**

   - Atomic writes using temp files + `os.replace()`
   - JSONL format for chunks (human-readable, line-by-line)
   - Pickle format for embeddings (efficient binary storage)
   - Batch files paired: `chunks-{timestamp}-part{N}.jsonl` + `embeddings-{timestamp}-part{N}.pkl`

3. **Database Transaction Management**

   - Centralized database client with connection pooling
   - Context-managed transactions with automatic rollback
   - Idempotent ingestion (duplicate detection prevents re-insertion)

4. **OCR Correction Pipeline**

   - LegalBERT-based grammar correction
   - Case-preserving replacements
   - Audit log of all corrections with confidence scores
   - 45 legal terms dictionary + 11 OCR-specific patterns

5. **Original Schema Preserved**
   - `documents` table: Document metadata
   - `document_versions` table: Version tracking with superseded_by references
   - `embeddings` table: Stores chunk_id, version_id, chunk_text, embedding_vector, extra_metadata

## ✨ Features

### Batch-Based Architecture (V5)

- 📁 **Folder-Driven Ingestion**: Drop PDFs in `SOURCE_DIR`, automatic discovery and processing
- � **Atomic Batch Files**: JSONL (chunks) + Pickle (embeddings) with atomic write operations
- 🔄 **Idempotent Processing**: Safe to re-run, automatic duplicate detection
- 🗄️ **Transaction Management**: Database operations with automatic rollback on failures
- 🔌 **Connection Pooling**: Efficient database connection reuse
- ✅ **Comprehensive Testing**: Unit tests for all modules + end-to-end integration tests

### Document Processing

- 📄 **PDF Extraction**: PyMuPDF-based text extraction with OCR fallback
- 🔍 **OCR Correction**: LegalBERT-based grammar correction with 45-term legal dictionary
- 🧹 **Text Cleaning**: Removes headers, footers, page numbers, formatting artifacts
- 📊 **Metadata Extraction**: Document title, jurisdiction, dates, version tracking
- 🗃️ **Batch Archival**: Source files archived after successful processing

### Advanced Chunking

- 🎯 **Token-Aware Chunking**: 400-800 tokens per chunk with 15% overlap
- 📏 **Context-Preserving**: Maintains document hierarchy and relationships
- � **Batch Generation**: Chunks written to JSONL files with metadata
- 💾 **Offline Processing**: No database interaction during chunking phase

### Embedding & Storage

- 🧮 **768-dimensional embeddings** using Ollama's nomic-embed-text
- 🐘 **PostgreSQL + pgvector**: High-performance vector storage
- 🔢 **Batch Ingestion**: Transactional loading from batch files
- 💾 **Original Schema**: Preserves V4 database structure (documents, document_versions, embeddings)
- 🏷️ **Version Tracking**: Full version history with superseded_by relationships

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

### V5 Batch Processing Workflow

```
┌──────────────────────────────────────────────────────────────────┐
│                   SOURCE_DIR (Legal PDFs)                        │
│              Folder-Driven Document Discovery                    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │ Folder Chunker   │
                    │  - PDF Extract   │
                    │  - Token Chunk   │
                    │  - Embed (Ollama)│
                    └────────┬────────┘
                             │
        ┌────────────────────┴────────────────────┐
        │         Batch Files (Atomic Write)       │
        │  chunks-{ts}-part{N}.jsonl (JSONL)      │
        │  embeddings-{ts}-part{N}.pkl (Pickle)    │
        └────────────────────┬────────────────────┘
                             │
                    ┌────────▼────────┐
                    │ OCR Corrector    │
                    │  - LegalBERT     │
                    │  - Legal Dict    │
                    │  - Audit Log     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Batch Ingestor   │
                    │  - Validate      │
                    │  - Transaction   │
                    │  - Deduplicate   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   PostgreSQL     │
                    │   + pgvector     │
                    │  ┌──────────┐    │
                    │  │documents │    │
                    │  │versions  │    │
                    │  │embeddings│    │
                    │  └──────────┘    │
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

### Module Architecture

```
processors/
├── folder_chunker.py      # Folder-driven PDF → batch files
├── ocr_corrector.py       # LegalBERT OCR correction
└── batch_ingestor.py      # Batch files → database

db/
├── pg_client.py           # Database client with pooling
└── sql.py                 # All SQL queries

utils/
└── batch_writer.py        # Atomic JSONL/Pickle writers

scripts/
├── test_db_transaction.py      # Database tests
├── test_batch_writer.py         # Writer tests
├── test_folder_chunker.py       # Chunker tests
├── test_ocr_corrector.py        # OCR tests
├── test_batch_ingestor.py       # Ingestor tests
└── test_end_to_end.py          # Full pipeline test
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

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/snjiraini/Langchain-and-Ollama.git
cd "Langchain-and-Ollama/17.2 RAG-V5 Improved batched processing"

# Activate conda environment
conda activate LLMTuning311

# Configure environment
cp .env.example .env
nano .env  # Update with your settings
```

### 2. Start Services

```bash
# Start PostgreSQL (if not running)
brew services start postgresql@18  # macOS
# or
sudo systemctl start postgresql     # Linux

# Start Ollama
ollama serve

# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

### 3. Run Batch Processing Pipeline

**Option A: Use Python Scripts**

```bash
# Step 1: Process PDFs to batch files (folder-driven)
python -c "from processors.folder_chunker import create_chunker_from_env; chunker = create_chunker_from_env(); chunker.process_all_files()"

# Step 2: Ingest batch files to database
python -c "from processors.batch_ingestor import create_ingestor_from_env; ingestor = create_ingestor_from_env(); ingestor.ingest_all_batches()"

# Step 3: Verify ingestion
python scripts/test_end_to_end.py
```

**Option B: Use Jupyter Notebook**

```bash
# Open notebook
jupyter lab Legal_RAG_Pipeline_V5_Complete.ipynb

# Run cells in order:
# 1. Configuration cell (loads .env)
# 2. Import & setup cells
# 3. Process documents
# 4. Run batch ingestion
# 5. Test RAG system
```

### 4. Test the System

```python
# Quick test query
from langchain_community.vectorstores import PGVector
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model=os.getenv('EMBEDDING_MODEL', 'nomic-embed-text'),
    base_url=os.getenv('EMBEDDING_BASE_URL', 'http://localhost:11434')
)

vectorstore = PGVector(
    collection_name="legal_embeddings",
    connection_string=f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    embedding_function=embeddings
)

# Search documents
results = vectorstore.similarity_search("fundamental rights", k=5)
for doc in results:
    print(f"Content: {doc.page_content[:200]}...")
```

## � Batch Processing Workflow

### Complete Workflow Overview

```
PDFs in SOURCE_DIR → Folder Chunker → Batch Files → Batch Ingestor → PostgreSQL
```

### Folder-Driven Chunking

The folder chunker discovers PDFs in `SOURCE_DIR` and processes them:

```python
from processors.folder_chunker import FolderDrivenChunker

chunker = FolderDrivenChunker(
    source_dir='./rag-dataset/legal documents',
    batch_dir='./pipeline_storage/batches',
    archive_dir='./data/archive',
    min_chunk_tokens=400,
    max_chunk_tokens=800,
    chunk_overlap_pct=0.15
)

# Process all PDFs
results = chunker.process_all_files()
print(f"Processed: {results['processed']}/{results['total_files']}")
```

**Output:** Batch file pairs in `pipeline_storage/batches/`:

- `chunks-20251123-123045-part000.jsonl`
- `embeddings-20251123-123045-part000.pkl`

### Batch File Formats

**Chunks (JSONL):**

```json
{"chunk_id": "doc_abc_chunk_0000", "version_id": "v_xyz", "text": "Article 1...", "metadata": {...}}
```

**Embeddings (Pickle):**

```python
{
    'embeddings': [[0.1, 0.2, ...], ...],  # 768-dim vectors
    'metadata': [{'chunk_id': 'doc_abc_chunk_0000', 'version_id': 'v_xyz', ...}],
    'count': 10
}
```

### Batch Ingestion

Load batch files into PostgreSQL with transaction safety:

```python
from processors.batch_ingestor import BatchIngestor
from db.pg_client import DatabaseClient

db_client = DatabaseClient(dbname='rag_db', user='postgres')
ingestor = BatchIngestor(db_client=db_client, batch_dir='./pipeline_storage/batches')

results = ingestor.ingest_all_batches()
print(f"Ingested: {results['batches_ingested']} batches, {results['total_chunks']} chunks")
```

**Features:**

- ✅ Automatic validation (chunk/embedding count match)
- ✅ Transaction management (rollback on error)
- ✅ Idempotent (safe to re-run)
- ✅ Batch archival after success

## 🧪 Testing

### Run All Tests

```bash
# Activate conda environment
conda activate LLMTuning311

# Run all module tests
python scripts/test_db_transaction.py       # Database client tests
python scripts/test_batch_writer.py         # Batch writer tests
python scripts/test_folder_chunker.py       # Folder chunker tests
python scripts/test_ocr_corrector.py        # OCR corrector tests
python scripts/test_batch_ingestor.py       # Batch ingestor tests

# Run end-to-end integration test
python scripts/test_end_to_end.py
```

### Test Coverage

| Module          | Tests                                      | Status           |
| --------------- | ------------------------------------------ | ---------------- |
| Database Client | Transaction management, connection pooling | ✅ Passing       |
| Batch Writers   | Atomic writes, JSONL/Pickle format         | ✅ Passing       |
| Folder Chunker  | PDF processing, batch file creation        | ✅ Passing       |
| OCR Corrector   | Legal dictionary, patterns, audit log      | ✅ Passing (6/6) |
| Batch Ingestor  | Validation, ingestion, idempotency         | ✅ Passing (4/4) |
| End-to-End      | Complete pipeline with real PDFs           | ✅ Passing (3/3) |

### End-to-End Test Output

```bash
$ python scripts/test_end_to_end.py

======================================================================
LEGAL RAG PIPELINE V5 - END-TO-END INTEGRATION TEST
======================================================================

Test 1: Folder-Driven Chunking
  Files processed: 3
  Batch files: 3 pairs
  ✅ PASS

Test 2: Batch Ingestion
  Batches ingested: 3
  Chunks in DB: 3
  ✅ PASS

Test 3: Database Verification
  Documents: 3
  Embeddings: 3 (768-dim)
  ✅ PASS

🎉 ALL END-TO-END TESTS PASSED!
```

## ⚙️ Configuration

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

All configuration is managed via `.env` file. See [CONFIGURATION_MIGRATION.md](CONFIGURATION_MIGRATION.md) for complete guide.

### Quick Setup

```bash
# Copy template
cp .env.example .env

# Edit with your settings
nano .env
```

### Key Configuration Variables

**Database:**

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rag_db
DB_USER=your_username
DB_PASSWORD=your_password  # Optional for local
```

**Directories:**

```bash
SOURCE_DIR=./rag-dataset/legal documents
BATCH_FILE_DIR=./pipeline_storage/batches
ARCHIVE_DIR=./data/archive
LOG_DIR=./logs
```

**Embedding:**

```bash
EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_BASE_URL=http://localhost:11434
EMBEDDING_DIM=768
```

**Chunking:**

```bash
MIN_CHUNK_TOKENS=400
MAX_CHUNK_TOKENS=800
CHUNK_OVERLAP_PERCENTAGE=0.15
```

**OCR:**

```bash
LEGALBERT_MODEL=nlpaueb/legal-bert-base-uncased
LEGALBERT_CONFIDENCE_THRESHOLD=0.8
OCR_CONFIDENCE_THRESHOLD=0.6
```

**Batch Processing:**

```bash
BATCH_SIZE=500  # Records per database insert
```

See `.env.example` for complete list of all configuration variables.

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
17.2 RAG-V5 Improved batched processing/
├── Legal_RAG_Pipeline_V5_Complete.ipynb  # Main notebook
├── README.md                              # This file
├── CONFIGURATION_MIGRATION.md             # .env migration guide
├── requirements.txt                       # Python dependencies
├── .env.example                          # Environment template
├── .env                                  # Your configuration (gitignored)
│
├── db/                                   # Database module
│   ├── __init__.py
│   ├── pg_client.py                      # Connection pooling & transactions
│   └── sql.py                            # All SQL queries
│
├── processors/                           # Processing modules
│   ├── __init__.py
│   ├── folder_chunker.py                 # Folder-driven PDF→batch files
│   ├── ocr_corrector.py                  # LegalBERT OCR correction
│   └── batch_ingestor.py                 # Batch files→database
│
├── utils/                                # Utility modules
│   ├── __init__.py
│   └── batch_writer.py                   # Atomic JSONL/Pickle writers
│
├── scripts/                              # Test scripts
│   ├── test_db_transaction.py            # Database tests
│   ├── test_batch_writer.py              # Writer tests
│   ├── test_folder_chunker.py            # Chunker tests
│   ├── test_ocr_corrector.py             # OCR tests
│   ├── test_batch_ingestor.py            # Ingestor tests
│   └── test_end_to_end.py               # Full pipeline test
│
├── rag-dataset/                          # Source documents
│   └── legal documents/                  # PDFs placed here
│
├── pipeline_storage/                     # Pipeline artifacts
│   ├── batches/                          # Generated batch files
│   │   ├── chunks-*.jsonl
│   │   ├── embeddings-*.pkl
│   │   └── archived/                     # Ingested batches
│   ├── raw_files/                        # Raw extractions
│   ├── ocr_output/                       # OCR temp files
│   └── normalized/                       # Cleaned text
│
├── data/                                 # Processed data
│   └── archive/                          # Archived source PDFs
│
└── logs/                                 # Application logs
    └── ocr_corrections.log               # OCR audit trail
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

1. **Check the Logs**: Look for error messages in notebook output or log files
2. **Verify Setup**: Run `python scripts/test_end_to_end.py`
3. **Check Versions**: Ensure all dependencies match requirements
4. **Database State**: Query database to check data integrity
5. **Review Configuration**: Verify `.env` file has correct values
6. **Check Test Output**: Run individual module tests to isolate issues
7. **Open an Issue**: Create a GitHub issue with:
   - Error message and full stack trace
   - System info (OS, Python version, PostgreSQL version)
   - `.env.example` values (never share actual `.env`)
   - Steps to reproduce

## � Migration from V4

### Key Differences V4 → V5

| Aspect               | V4                          | V5                                  |
| -------------------- | --------------------------- | ----------------------------------- |
| **Processing Model** | Notebook-driven, sequential | Batch-based, folder-driven          |
| **File Operations**  | Direct writes               | Atomic temp file + replace          |
| **Database Access**  | Per-cell connections        | Centralized client with pooling     |
| **Chunking**         | Notebook cells              | Standalone `folder_chunker.py`      |
| **OCR**              | Inline corrections          | Dedicated `ocr_corrector.py` module |
| **Configuration**    | Hardcoded in cells          | `.env` file-based                   |
| **Testing**          | Manual notebook execution   | Automated unit + integration tests  |
| **Error Handling**   | Manual rollback             | Automatic transaction management    |
| **Idempotency**      | Not guaranteed              | Built-in duplicate detection        |

### Migration Steps

1. **Backup V4 Data**

   ```bash
   pg_dump legalrag_v4_db > v4_backup.sql
   ```

2. **Setup V5 Environment**

   ```bash
   cp .env.example .env
   nano .env  # Configure settings
   ```

3. **Run V5 Pipeline**

   ```bash
   # Place PDFs in SOURCE_DIR
   python scripts/test_end_to_end.py
   ```

4. **Verify Migration**

   ```sql
   -- Check document count
   SELECT COUNT(*) FROM documents;

   -- Check embedding dimensions
   SELECT COUNT(*), AVG(array_length(embedding_vector, 1))
   FROM embeddings;
   ```

### Schema Compatibility

V5 preserves the original V4 schema:

- ✅ `documents` table structure unchanged
- ✅ `document_versions` table structure unchanged
- ✅ `embeddings` table structure unchanged
- ✅ All V4 queries work in V5

**Note:** V5 can read existing V4 data. Simply configure V5 to point to your V4 database.

## 🤝 Contributing

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
- **LegalBERT**: For legal text understanding

## 📧 Contact

- **Author**: Samuel Njiraini
- **Repository**: [Langchain-and-Ollama](https://github.com/snjiraini/Langchain-and-Ollama)
- **Issues**: [GitHub Issues](https://github.com/snjiraini/Langchain-and-Ollama/issues)

## 🔮 Future Enhancements

- [ ] Streaming ingestion for real-time updates
- [ ] Parallel batch processing
- [ ] Incremental updates (delta processing)
- [ ] Multi-language support
- [ ] Hybrid search (keyword + semantic)
- [ ] Web UI for batch monitoring
- [ ] REST API for batch operations
- [ ] Batch scheduling (cron/airflow)
- [ ] Advanced OCR models (Tesseract, cloud OCR)
- [ ] Document comparison and diff detection
- [ ] Custom embedding models
- [ ] Analytics dashboard for batch metrics

---

**Built with ❤️ for legal professionals and researchers**

_Last Updated: November 23, 2025_  
_Version: V5 (Batch Processing Architecture)_
