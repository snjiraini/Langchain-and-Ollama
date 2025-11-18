# Quick Start Guide - RAG with FAISS

Get your RAG system running in 3 minutes.

## Prerequisites Checklist

- [ ] Conda environment: `LLMTuning311`
- [ ] Ollama running with models pulled

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
conda activate LLMTuning311
pip install -r requirements.txt
```

### 2. Install Ollama Models

```bash
# Start Ollama (in a separate terminal)
ollama serve

# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2:3b

# Verify models
ollama list
```

### 3. Run the Notebook

```bash
jupyter notebook "RAG - Chat with Kenyan Consitution v3.ipynb"
```

**Important:** Run cells in order. Document ingestion takes 10-20 minutes on first run.

## Quick Commands

### Ollama Service

```bash
# Start Ollama
ollama serve

# Check models
ollama list

# Test embedding model
ollama run nomic-embed-text "test"

# Test LLM
ollama run llama3.2:3b "Hello"
```

### Check FAISS Index

```bash
# Check if index exists
ls -lh legal_documents/faiss_index/

# Index files
# - index.faiss (vector index)
# - index.pkl (document store)
```

## Troubleshooting

### Ollama connection error

```bash
# Restart Ollama
pkill ollama && ollama serve

# Check if models are installed
ollama list
```

### Python import errors

```bash
conda activate LLMTuning311
pip install -r requirements.txt --upgrade
```

### FAISS index not found

Run the ingestion cell in the notebook (Cell ~22-25). This creates the index on first run.

### Out of memory during ingestion

- Restart Ollama: `pkill ollama && ollama serve`
- Close other applications
- Wait a few minutes and retry

## Next Steps

1. **Load documents** - Run notebook cells 1-15 to load and parse PDFs
2. **Chunk documents** - Run semantic chunking cells (2-3 minutes)
3. **Create vector index** - Run FAISS ingestion cells (10-20 minutes, one-time)
4. **Query system** - Run retrieval cells to ask questions (instant)

## Expected Timeline

| Task                  | Time      | Notes                          |
| --------------------- | --------- | ------------------------------ |
| Install dependencies  | 2 min     | One-time setup                 |
| Install Ollama models | 3 min     | One-time download              |
| Load documents        | 1 min     | Cells 1-15                     |
| Semantic chunking     | 2-3 min   | Context-aware splitting        |
| Create FAISS index    | 10-20 min | One-time ingestion             |
| Query system          | <1 sec    | Instant after index is created |

## Performance Tips

- **First time ingestion takes 10-20 minutes** - This is normal for embedding generation
- **Subsequent queries are fast** - Usually 50-200ms per query
- **Save your index** - Use `vector_store.save_local()` to persist vectors
- **Load existing index** - Use `FAISS.load_local()` to skip re-ingestion
- **Monitor Ollama** - If it hangs, restart: `pkill ollama && ollama serve`

## FAISS Index Management

### Save Index

```python
# In notebook
vector_store.save_local("legal_documents/faiss_index")
```

### Load Existing Index

```python
# In notebook
from langchain_community.vectorstores import FAISS

vector_store = FAISS.load_local(
    "legal_documents/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

print(f"Loaded {vector_store.index.ntotal} vectors")
```

### Delete Index

```bash
# Remove index files
rm -rf legal_documents/faiss_index/
```

## Getting Help

- **Check Ollama**: `ollama list` to verify models
- **Check index**: `ls -lh legal_documents/faiss_index/`
- **Review logs**: Check notebook cell outputs for errors
- **Detailed docs**: See [README.md](README.md) for technical information

---

**Ready?** Run these commands to start:

```bash
conda activate LLMTuning311
jupyter notebook
```

If Ollama is running and models are installed, you're ready to go! 🚀

## What's Different from v2?

This version uses **context-aware semantic chunking** instead of fixed-size chunks:

- **v2**: Fixed 1000-character chunks with 200-character overlap
- **v3**: Intelligent semantic boundaries based on sentence similarity

Result: Better retrieval accuracy and more coherent context for answers.
