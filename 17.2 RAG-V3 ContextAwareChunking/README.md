# RAG System with FAISS - Kenyan Constitution Q&A# RAG System with FAISS - Kenyan Constitution Q&A

A local-first Retrieval-Augmented Generation (RAG) system for querying the Kenyan Constitution using FAISS, LangChain, Ollama, and context-aware semantic chunking.A local-first Retrieval-Augmented Generation (RAG) system for querying the Kenyan Constitution using FAISS, LangChain, Ollama, and context-aware semantic chunking.

## 🌟 Features## 🌟 Features

- **Context-Aware Semantic Chunking** - Intelligent document splitting based on semantic similarity- **Context-Aware Semantic Chunking** - Intelligent document splitting based on semantic similarity

- **FAISS Backend** - Fast, local vector storage with no database dependencies- **FAISS Backend** - Fast, local vector storage with no database dependencies

- **Simple Setup** - No PostgreSQL required, vectors stored as local files- **Simple Setup** - No PostgreSQL required, vectors stored as local files

- **Ollama Integration** - Local LLM inference with llama3.2 and nomic-embed-text- **Ollama Integration** - Local LLM inference with llama3.2 and nomic-embed-text

- **Flexible Retrieval** - Multiple search strategies (similarity, MMR, score threshold)- **Flexible Retrieval** - Multiple search strategies (similarity, MMR, score threshold)

- **Persistent Storage** - Save and load vector indices from disk- **Persistent Storage** - Save and load vector indices from disk

## 🚀 Quick Start## 🚀 Quick Start

See **[QUICKSTART.md](QUICKSTART.md)** for a 3-minute setup guide.See **[QUICKSTART.md](QUICKSTART.md)** for a 3-minute setup guide.

### Prerequisites### Prerequisites

- Python 3.11+ (Conda environment: `LLMTuning311`)- Python 3.11+ (Conda environment: `LLMTuning311`)

- Ollama with required models (`nomic-embed-text`, `llama3.2:3b`)- Ollama with required models (`nomic-embed-text`, `llama3.2:3b`)

## 📁 Project Structure## 📁 Project Structure

````

17.2 RAG-V3 ContextAwareChunking/17.2 RAG-V3 ContextAwareChunking/

├── RAG - Chat with Kenyan Consitution v3.ipynb  # Main notebook├── RAG - Chat with Kenyan Consitution v3.ipynb  # Main notebook

├── 07_context_aware_chunking_complete.py        # Reference implementation├── 07_context_aware_chunking_complete.py        # Reference implementation

├── app.py                                       # Streamlit app├── init_db.py                                   # Database setup script

├── requirements.txt                             # Python dependencies├── verify_setup.py                              # System verification tool

├── QUICKSTART.md                                # Setup guide├── app.py                                       # Streamlit app

├── README.md                                    # This file├── requirements.txt                             # Python dependencies

├── legal_documents/                             # Source PDF documents├── .env.example                                 # Environment template

│   └── faiss_index/                            # FAISS vector index (auto-created)├── QUICKSTART.md                                # Setup guide

└── rag-dataset/                                 # Document corpus├── README.md                                    # This file

```├── legal_documents/                             # Source PDF documents

└── rag-dataset/                                 # Document corpus

## ⚙️ Configuration```



### Ollama Setup## � Configuration



Ensure Ollama is running with the required models:### Environment Variables (.env)



```bashCreate a `.env` file from the template:

# Start Ollama

ollama serve```bash

cp .env.example .env

# Pull required models```

ollama pull nomic-embed-text  # 768-dimensional embeddings

ollama pull llama3.2:3b       # Language model for responsesConfiguration options:

```

```bash

### Vector Storage# PostgreSQL Configuration

DB_NAME=rag_db

FAISS stores vectors in the `legal_documents/faiss_index/` directory:DB_USER=your_username      # Your macOS username

DB_HOST=localhost

- `index.faiss` - Vector index fileDB_PORT=5432

- `index.pkl` - Document store and metadataDB_PASSWORD=               # Optional, leave empty for local dev



The index is automatically created when you run the ingestion cell in the notebook.# Ollama Configuration

OLLAMA_BASE_URL=http://localhost:11434

## 🔧 Technical ImplementationOLLAMA_EMBED_MODEL=nomic-embed-text

OLLAMA_LLM_MODEL=llama3.2:3b

### 1. Context-Aware Semantic Chunking```



Unlike fixed-size chunking, this system intelligently splits documents at semantic boundaries:### Database Schema



```pythonThe system uses a PostgreSQL database with pgvector extension:

def semantic_chunk(docs, embeddings, similarity_threshold=0.8):

    """```sql

    Chunks documents based on semantic similarity between sentences.-- Enable pgvector extension

CREATE EXTENSION IF NOT EXISTS vector;

    Args:

        docs: List of LangChain Document objects-- Create chunks table

        embeddings: OllamaEmbeddings instanceCREATE TABLE chunks (

        similarity_threshold: Cosine similarity threshold (0-1)    id SERIAL PRIMARY KEY,

            - Higher threshold = fewer splits (larger chunks)    content TEXT NOT NULL,

            - Lower threshold = more splits (smaller chunks)    embedding vector(768) NOT NULL,  -- 768-dim for nomic-embed-text

    metadata JSONB,

    Returns:    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        List of semantically coherent Document chunks);



    Process:-- Create vector similarity index (IVFFlat for fast approximate search)

        1. Split document into sentencesCREATE INDEX chunks_embedding_idx

        2. Generate embeddings for each sentenceON chunks USING ivfflat (embedding vector_cosine_ops)

        3. Calculate cosine similarity between consecutive sentencesWITH (lists = 100);

        4. Create new chunk when similarity drops below threshold```

        5. Preserves topic coherence within chunks

    """**Schema Notes:**

```

- `embedding vector(768)`: Matches nomic-embed-text output dimensions

**Benefits:**- `metadata JSONB`: Stores source file, page numbers, etc.

- `IVFFlat index`: Enables fast similarity search (100 lists suitable for 10K-100K vectors)

- Preserves contextual meaning and topic boundaries

- Avoids cutting concepts mid-sentence## � Technical Implementation

- Improves retrieval relevance (related content stays together)

- Better RAG responses with complete context### 1. Context-Aware Semantic Chunking



### 2. Document Ingestion PipelineUnlike fixed-size chunking, this system intelligently splits documents at semantic boundaries:



```python```python

# Load documentsdef semantic_chunk(docs, embeddings, similarity_threshold=0.8):

from langchain_community.document_loaders import PyMuPDFLoader    """

docs = PyMuPDFLoader("legal_documents/constitution.pdf").load()    Chunks documents based on semantic similarity between sentences.



# Apply semantic chunking    Args:

chunks = semantic_chunk(docs, embeddings, similarity_threshold=0.8)        docs: List of LangChain Document objects

        embeddings: OllamaEmbeddings instance

# Create FAISS vector store        similarity_threshold: Cosine similarity threshold (0-1)

from langchain_community.vectorstores import FAISS            - Higher threshold = fewer splits (larger chunks)

            - Lower threshold = more splits (smaller chunks)

vector_store = FAISS(

    embedding_function=embeddings,    Returns:

    index=index,        List of semantically coherent Document chunks

    docstore=InMemoryDocstore(),

    index_to_docstore_id={}    Process:

)        1. Split document into sentences

        2. Generate embeddings for each sentence

# Add documents to vector store        3. Calculate cosine similarity between consecutive sentences

ids = vector_store.add_documents(documents=chunks)        4. Create new chunk when similarity drops below threshold

        5. Preserves topic coherence within chunks

# Save to disk    """

vector_store.save_local("legal_documents/faiss_index")```

```

**Benefits:**

**Performance Characteristics:**

- Preserves contextual meaning and topic boundaries

- **Ingestion Time**: 10-20 minutes for full Kenyan Constitution corpus- Avoids cutting concepts mid-sentence

- **Storage**: ~50-100MB for index files- Improves retrieval relevance (related content stays together)

- **No Database**: All data stored as local files- Better RAG responses with complete context



### 3. Vector Similarity Search### 2. Document Ingestion Pipeline



FAISS provides multiple search strategies:```python

# Load documents

```pythonfrom langchain_community.document_loaders import PyMuPDFLoader

# Basic similarity searchdocs = PyMuPDFLoader("legal_documents/constitution.pdf").load()

docs = vector_store.similarity_search(query="What are fundamental rights?", k=5)

# Apply semantic chunking

# Search with score thresholdchunks = semantic_chunk(docs, embeddings, similarity_threshold=0.8)

docs = vector_store.similarity_search_with_score(

    query="What are fundamental rights?",# Store in pgvector with batch processing

    k=5for chunk in chunks:

)    # Generate embedding

    embedding = embeddings.embed_query(chunk.page_content)

# Maximum Marginal Relevance (MMR) search

docs = vector_store.max_marginal_relevance_search(    # Insert into database

    query="What are fundamental rights?",    cur.execute(

    k=3,        'INSERT INTO chunks (content, embedding, metadata) VALUES (%s, %s, %s)',

    fetch_k=20        (chunk.page_content, embedding, json.dumps(chunk.metadata))

)    )

```

conn.commit()

### 4. Retriever Configuration```



Integration with LangChain's RAG pipeline:**Performance Characteristics:**



```python- **Batch Size**: 5 chunks per batch (prevents Ollama overload)

# Basic similarity retriever- **Retry Logic**: Automatic retry with exponential backoff

retriever = vector_store.as_retriever(- **Time**: 10-20 minutes for full Kenyan Constitution corpus

    search_type='similarity',- **Error Handling**: Failed chunks logged for manual review

    search_kwargs={'k': 3}

)### 3. Vector Similarity Search



# Similarity with score threshold```python

retriever = vector_store.as_retriever(def search_similar_chunks(query: str, k: int = 3, score_threshold: float = 0.0):

    search_type='similarity_score_threshold',    """

    search_kwargs={'k': 3, 'score_threshold': 0.5}    Search for similar chunks using pgvector cosine similarity.

)

    Args:

# MMR retriever (diversity-aware)        query: User question

retriever = vector_store.as_retriever(        k: Number of chunks to retrieve

    search_type='mmr',        score_threshold: Minimum similarity score (0-1)

    search_kwargs={'k': 3, 'fetch_k': 20, 'lambda_mult': 1}

)    Returns:

```        List of (id, content, metadata, similarity_score) tuples

    """

**Retriever Parameters:**    query_embedding = embeddings.embed_query(query)



- `k`: Number of documents to retrieve    with conn.cursor() as cur:

- `score_threshold`: Minimum similarity score (0-1)        cur.execute('''

- `fetch_k`: Number of candidates for MMR (higher = more diverse)            SELECT id, content, metadata,

- `lambda_mult`: MMR diversity factor (0=max diversity, 1=max relevance)                   1 - (embedding <=> %s::vector) as similarity

            FROM chunks

### 5. RAG Pipeline            WHERE 1 - (embedding <=> %s::vector) >= %s

            ORDER BY embedding <=> %s::vector

```python            LIMIT %s

from langchain_ollama import ChatOllama        ''', (query_embedding, query_embedding, score_threshold, query_embedding, k))

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser        return cur.fetchall()

from langchain_core.runnables import RunnablePassthrough```



# Initialize components**Similarity Operators:**

retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})

llm = ChatOllama(model='llama3.2:3b', base_url='http://localhost:11434')- `<=>` : Cosine distance (recommended for normalized embeddings)

- `<->` : L2/Euclidean distance

# Create prompt template- `<#>` : Inner product (for non-normalized embeddings)

prompt = ChatPromptTemplate.from_template("""

You are an assistant for question-answering tasks. Use the following pieces of### 4. Custom LangChain Retriever

retrieved context to answer the question. If you don't know the answer, just say

that you don't know. Answer in bullet points. Make sure your answer is relevantIntegration with LangChain's RAG pipeline:

to the question and it is answered from the context only.

```python

Question: {question}from langchain_core.retrievers import BaseRetriever

Context: {context}from langchain.schema import Document

Answer:

""")class PgVectorRetriever(BaseRetriever):

    """Custom retriever for pgvector database."""

# Build RAG chain

def format_docs(docs):    conn: object           # PostgreSQL connection

    return '\n\n'.join([doc.page_content for doc in docs])    embeddings: object     # OllamaEmbeddings instance

    k: int = 3            # Number of documents to retrieve

rag_chain = (    score_threshold: float = 0.0  # Minimum similarity threshold

    {"context": retriever | format_docs, "question": RunnablePassthrough()}

    | prompt    class Config:

    | llm        arbitrary_types_allowed = True

    | StrOutputParser()

)    def _get_relevant_documents(self, query: str) -> List[Document]:

        """Retrieve relevant documents from pgvector."""

# Query the system        query_embedding = self.embeddings.embed_query(query)

question = "What are the fundamental rights and freedoms?"

response = rag_chain.invoke(question)        with self.conn.cursor() as cur:

print(response)            cur.execute('''

```                SELECT content, metadata,

                       1 - (embedding <=> %s::vector) as similarity

## 🎯 Performance & Scaling                FROM chunks

                WHERE 1 - (embedding <=> %s::vector) >= %s

### Query Performance                ORDER BY embedding <=> %s::vector

                LIMIT %s

| Metric                | Value           | Notes                             |            ''', (query_embedding, query_embedding,

| --------------------- | --------------- | --------------------------------- |                  self.score_threshold, query_embedding, self.k))

| **Query Latency**     | 50-200ms        | Much faster than database queries |

| **Index Type**        | Flat L2         | Exact nearest neighbor search     |            results = cur.fetchall()

| **Similarity Metric** | L2 distance     | Normalized to cosine similarity   |

| **Concurrent Users**  | Single process  | Use multiple processes for scale  |        # Convert to LangChain Document objects

        documents = []

### Index Types        for content, metadata, similarity in results:

            doc = Document(

FAISS supports multiple index types:                page_content=content,

                metadata=json.loads(metadata) if metadata else {}

```python            )

# Flat L2 (exact search, good for <1M vectors) - DEFAULT            documents.append(doc)

index = faiss.IndexFlatL2(dimension)

        return documents

# IVF (approximate search, faster for large datasets)```

quantizer = faiss.IndexFlatL2(dimension)

index = faiss.IndexIVFFlat(quantizer, dimension, nlist=100)### 5. RAG Pipeline

index.train(training_vectors)  # Required for IVF

```python

# HNSW (hierarchical graph, best for large-scale)from langchain_ollama import ChatOllama

index = faiss.IndexHNSWFlat(dimension, M=32)from langchain_core.prompts import ChatPromptTemplate

```from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnablePassthrough

### Storage Management

# Initialize components

**Save Index:**retriever = PgVectorRetriever(conn=conn, embeddings=embeddings, k=3)

llm = ChatOllama(model='llama3.2:3b', base_url='http://localhost:11434')

```python

vector_store.save_local("legal_documents/faiss_index")# Create prompt template

```prompt = ChatPromptTemplate.from_template("""

You are an assistant for question-answering tasks. Use the following pieces of

**Load Index:**retrieved context to answer the question. If you don't know the answer, just say

that you don't know. Answer in bullet points. Make sure your answer is relevant

```pythonto the question and it is answered from the context only.

vector_store = FAISS.load_local(

    "legal_documents/faiss_index",Question: {question}

    embeddings,Context: {context}

    allow_dangerous_deserialization=TrueAnswer:

)""")

```

# Build RAG chain

**Check Status:**def format_docs(docs):

    return '\n\n'.join([doc.page_content for doc in docs])

```python

# Number of vectorsrag_chain = (

print(f"Total vectors: {vector_store.index.ntotal}")    {"context": retriever | format_docs, "question": RunnablePassthrough()}

    | prompt

# Index size in memory    | llm

import sys    | StrOutputParser()

print(f"Index size: {sys.getsizeof(vector_store.index)} bytes"))

```

# Query the system

## 🛠️ Troubleshootingquestion = "What are the fundamental rights and freedoms?"

response = rag_chain.invoke(question)

### Ollama Issuesprint(response)

```

**Connection Timeout:**

## 🎯 Performance & Scaling

```bash

# Restart Ollama### Query Performance

pkill ollama && ollama serve

| Metric                | Value           | Notes                             |

# Check status| --------------------- | --------------- | --------------------------------- |

ollama list| **Query Latency**     | 100-500ms       | Depends on k value and index size |

| **Index Type**        | IVFFlat         | Approximate nearest neighbor      |

# Test embedding model| **Similarity Metric** | Cosine distance | Best for normalized embeddings    |

ollama run nomic-embed-text "test"| **Concurrent Users**  | Unlimited       | PostgreSQL connection pooling     |

```

### Index Tuning

**Models Not Found:**

Adjust IVFFlat `lists` parameter based on dataset size:

```bash

# Pull required models```sql

ollama pull nomic-embed-text-- Small dataset (<10K chunks)

ollama pull llama3.2:3bCREATE INDEX chunks_embedding_idx

ON chunks USING ivfflat (embedding vector_cosine_ops)

# Verify models installedWITH (lists = 10);

ollama list

```-- Medium dataset (10K-100K chunks) - DEFAULT

WITH (lists = 100);

### FAISS Issues

-- Large dataset (100K-1M chunks)

**Index Not Found:**WITH (lists = 1000);



```python-- Very large dataset (1M+ chunks)

# Check if index existsWITH (lists = 5000);

import os```

if os.path.exists("legal_documents/faiss_index/index.faiss"):

    print("✅ Index found")**Rebuild Index:**

else:

    print("❌ Index not found - run ingestion cell")```sql

```DROP INDEX chunks_embedding_idx;

CREATE INDEX chunks_embedding_idx

**Out of Memory:**ON chunks USING ivfflat (embedding vector_cosine_ops)

WITH (lists = 1000);

- Use IVFFlat index for large datasets (>100K chunks)ANALYZE chunks;

- Reduce batch size during ingestion```

- Increase swap space on your system

### Database Maintenance

### Performance Issues

**Backup:**

**Slow Ingestion:**

```bash

- Reduce `batch_size` (default: 5)# Backup database

- Restart Ollama if unresponsivepg_dump rag_db > backup_$(date +%Y%m%d).sql

- Check CPU/RAM usage

# Restore database

**Slow Queries:**psql -d rag_db < backup_20250117.sql

```

- Use IVFFlat or HNSW index for large datasets

- Reduce `k` value (number of results)**Clear Data:**

- Consider caching frequently asked questions

```sql

## 📝 Example Usage-- Delete all chunks (preserves table structure)

TRUNCATE TABLE chunks;

### Basic Query

-- Reset auto-increment counter

```pythonALTER SEQUENCE chunks_id_seq RESTART WITH 1;

question = "What is the sovereignty of the people?"```

response = rag_chain.invoke(question)

print(response)**Check Status:**

```

```sql

### Advanced Query with Score Threshold-- Chunk count

SELECT COUNT(*) FROM chunks;

```python

retriever = vector_store.as_retriever(-- Database size

    search_type='similarity_score_threshold',SELECT pg_size_pretty(pg_database_size('rag_db')) as db_size;

    search_kwargs={'k': 5, 'score_threshold': 0.5}

)-- Table size

SELECT pg_size_pretty(pg_total_relation_size('chunks')) as table_size;

question = "What are the fundamental rights and freedoms?"

docs = retriever.invoke(question)-- Recent insertions

SELECT id, LEFT(content, 50) as preview, created_at

for idx, doc in enumerate(docs, 1):FROM chunks

    print(f"\n{idx}. {doc.page_content[:200]}...")ORDER BY created_at DESC

```LIMIT 5;



### Direct Search with Scores-- Index statistics

SELECT schemaname, tablename, indexname,

```python       pg_size_pretty(pg_relation_size(indexrelid)) as index_size

docs_with_scores = vector_store.similarity_search_with_score(FROM pg_stat_user_indexes

    query="What are fundamental rights?",WHERE tablename = 'chunks';

    k=5```

)

## � Troubleshooting

for doc, score in docs_with_scores:

    print(f"Score: {score:.4f}")### PostgreSQL Issues

    print(f"Content: {doc.page_content[:100]}...\n")

```**Connection Error:**



## 📚 Additional Resources```bash

# Check if PostgreSQL is running

- **FAISS Documentation**: https://github.com/facebookresearch/faissbrew services list | grep postgresql

- **LangChain RAG Guide**: https://python.langchain.com/docs/use_cases/question_answering/

- **Ollama Models**: https://ollama.ai/library# Start PostgreSQL

brew services start postgresql@18

## 🤝 Contributing

# Test connection

Contributions welcome! Please:psql -d postgres -c "SELECT version();"

```

1. Follow the existing code patterns from v2 notebook

2. Include error handling**pgvector Extension Not Found:**

3. Update documentation for new features

```bash

## ⚖️ Legal Disclaimer# Reinstall pgvector

brew reinstall pgvector

This application provides AI-generated analysis of legal documents for informational purposes only. Always consult with qualified legal professionals for authoritative legal advice.

# Enable extension in database

## 📄 Licensepsql -d rag_db -c "CREATE EXTENSION IF NOT EXISTS vector;"

```

This project is part of the Langchain-and-Ollama learning repository.

**Permission Denied:**

---

```bash

**Last Updated**: January 2025  # Grant database creation permission

**Python**: 3.11+  psql -d postgres -c "ALTER USER $(whoami) CREATEDB;"

**FAISS**: Latest

**Ollama**: Latest# Check current user

echo $USER  # Use this as DB_USER in .env
```

### Ollama Issues

**Connection Timeout:**

```bash
# Restart Ollama
pkill ollama && ollama serve

# Check status
ollama list

# Test embedding model
ollama run nomic-embed-text "test"
```

**Models Not Found:**

```bash
# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2:3b

# Verify models installed
ollama list
```

### Performance Issues

**Slow Queries:**

```sql
-- Analyze query plan
EXPLAIN ANALYZE
SELECT content FROM chunks
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 3;

-- Rebuild index with more lists
DROP INDEX chunks_embedding_idx;
CREATE INDEX chunks_embedding_idx
ON chunks USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 1000);

-- Update table statistics
ANALYZE chunks;
```

**Out of Memory During Ingestion:**

- Reduce `batch_size` in ingestion cell (default: 5)
- Increase `delay_between_batches` (default: 0.5s)
- Restart Ollama if unresponsive

## 📝 Example Usage

### Basic Query

```python
question = "What is the sovereignty of the people?"
response = rag_chain.invoke(question)
print(response)
```

### Advanced Query with Score Threshold

```python
retriever = PgVectorRetriever(
    conn=conn,
    embeddings=embeddings,
    k=5,
    score_threshold=0.5  # Only return docs with >50% similarity
)

question = "What are the fundamental rights and freedoms?"
docs = retriever.invoke(question)

for idx, doc in enumerate(docs, 1):
    print(f"\n{idx}. {doc.page_content[:200]}...")
```

### Direct Database Query

```python
def search_with_metadata(query: str, source_file: str = None):
    """Search with optional metadata filtering."""
    query_embedding = embeddings.embed_query(query)

    sql = '''
        SELECT content, metadata, 1 - (embedding <=> %s::vector) as similarity
        FROM chunks
        WHERE 1 = 1
    '''
    params = [query_embedding]

    if source_file:
        sql += " AND metadata->>'source' = %s"
        params.append(source_file)

    sql += " ORDER BY embedding <=> %s::vector LIMIT %s"
    params.extend([query_embedding, 5])

    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()
```

## � Security Considerations

- **Database Credentials**: Store in `.env` file, never commit to git
- **SQL Injection**: Use parameterized queries (already implemented)
- **Connection Pooling**: Configure in production environments
- **Network Security**: Use SSL for remote PostgreSQL connections

## 📚 Additional Resources

- **pgvector Documentation**: https://github.com/pgvector/pgvector
- **LangChain RAG Guide**: https://python.langchain.com/docs/use_cases/question_answering/
- **Ollama Models**: https://ollama.ai/library
- **PostgreSQL Performance**: https://www.postgresql.org/docs/current/performance-tips.html

## 🤝 Contributing

Contributions welcome! Please:

1. Follow the existing code patterns from `07_context_aware_chunking_complete.py`
2. Use environment variables for configuration
3. Include error handling and retries
4. Update documentation for new features

## ⚖️ Legal Disclaimer

This application provides AI-generated analysis of legal documents for informational purposes only. Always consult with qualified legal professionals for authoritative legal advice.

## � License

This project is part of the Langchain-and-Ollama learning repository.

---

**Last Updated**: November 17, 2025
**Python**: 3.11+
**PostgreSQL**: 18+
**pgvector**: 0.2.0+
````
