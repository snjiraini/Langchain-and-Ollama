# 🏛️ Kenyan Constitution RAG Chat - Streamlit App

A Streamlit web application that implements a RAG (Retrieval-Augmented Generation) system for chatting with the Kenyan Constitution using Llama3.2.

## 🚀 Features

- **Simple RAG Pipeline**: Uses Llama3.2 for question answering based on Constitution documents
- **Interactive Chat Interface**: Natural conversation with the Constitution documents
- **Performance Monitoring**: Real-time statistics for efficiency
- **Intermediate Steps Visualization**: Optional display of document retrieval
- **Session Management**: Persistent chat history during the session

## 🏗️ Architecture

1. **Document Retrieval**: FAISS vector store searches relevant Constitution sections
2. **Question Answering**: Llama3.2 processes retrieved context and questions to generate responses

## 📋 Prerequisites

### Required Services

- **Ollama** running locally on port 11434 with the following models:
  - `nomic-embed-text` (for embeddings)
  - `llama3.2:3b` (for response generation)

### Vector Store

- Pre-built FAISS vector store in `legal_documents/` directory
- Constitution documents in `rag-dataset/` directory

## 🛠️ Installation

1. **Clone and navigate to the directory**:

```bash
cd "17.2 RAG-Chat with Kenyan Constitution v2"
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Ensure Ollama is running**:

```bash
# Start Ollama service
ollama serve

# Pull required models (if not already available)
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

4. **Verify vector store exists**:

```bash
# The following files should exist:
# legal_documents/index.faiss
# legal_documents/index.pkl
```

## 🚀 Running the App

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 🎯 Usage

### Basic Chat

1. Type your question about the Kenyan Constitution in the chat input
2. Wait for the hybrid AI pipeline to process your query
3. View the refined response with legal insights

### Advanced Features Usage

#### Enable Intermediate Steps

1. Check "Show intermediate steps" in the sidebar
2. Ask any question
3. Expand "🔍 Intermediate Steps" to see:
   - Retrieved context from Constitution

#### Monitor Performance

1. Click "📊 Show Performance Stats" in sidebar
2. View metrics:
   - Total queries processed
   - Average response time

### Example Questions

- "What does the Constitution say about sovereignty of the people?"
- "What are the fundamental rights and freedoms?"
- "How is the government structured according to the Constitution?"
- "What does the Constitution say about citizenship?"

## ⚙️ Configuration

### Model Settings

```python
# Default configurations (can be customized in app.py)
EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3.2:3b"
RETRIEVAL_K = 3  # Number of documents to retrieve
```

### Performance Optimization

- Intelligent caching at all pipeline stages
- Device-aware model placement
- Chunked document processing
- Session state management

## 🔧 Troubleshooting

### Common Issues

1. **Ollama Connection Error**:

   - Ensure Ollama is running: `ollama serve`
   - Check if models are available: `ollama list`

2. **FAISS Vector Store Not Found**:

   - Verify `legal_documents/` directory exists
   - Check that `index.faiss` and `index.pkl` files are present

3. **Model Loading Issues**:

   - LegalBERT will automatically fallback to DistilBERT if unavailable
   - Check available device memory for large models

4. **Performance Issues**:
   - Enable GPU acceleration if available
   - Monitor performance stats in sidebar

### Dependencies Issues

```bash
# If you encounter package conflicts, try creating a new environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📊 Performance Monitoring

The app includes comprehensive performance tracking:

- **Response Times**: Processing duration for each query
- **Cache Efficiency**: Hit rates for different pipeline stages
- **Device Utilization**: Memory usage and device selection
- **Query Statistics**: Total queries processed

## ⚖️ Legal Disclaimer

This application provides AI-generated analysis of legal documents for informational purposes only. Always consult with qualified legal professionals for authoritative legal advice.

## 🤝 Contributing

To contribute improvements:

1. Test changes with the existing Constitution dataset
2. Ensure compatibility with the hybrid pipeline architecture
3. Maintain performance monitoring capabilities
4. Update documentation as needed

## 📝 License

This project is part of the Langchain-and-Ollama learning repository. Please refer to the main repository license.
