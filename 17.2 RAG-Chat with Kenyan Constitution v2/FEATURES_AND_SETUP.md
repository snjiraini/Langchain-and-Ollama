# 🏛️ Kenyan Constitution RAG Chat - Features & Setup Guide

## 🌟 Key Features

### 🤖 Hybrid AI Architecture

- **Two-Stage Processing**:
  - Stage 1: LegalBERT analyzes legal context with domain expertise
  - Stage 2: Llama3.2 refines responses for clarity and readability
- **Smart Retrieval**: FAISS vector store finds relevant Constitution sections
- **Performance Optimization**: Real-time performance monitoring

### 💬 Interactive Chat Interface

- **Natural Conversation**: Ask questions in plain English
- **Persistent History**: Chat messages saved during session
- **Real-time Processing**: Live response generation with progress indicators
- **Message Threading**: Clear conversation flow with user/assistant distinction

### ⚡ Performance & Monitoring

- **Response Time Tracking**: Monitor processing duration for each query
- **Cache Analytics**: View hit rates and efficiency metrics
- **Memory Management**: Automatic cache clearing and optimization
- **Device Optimization**: Auto-detection of CUDA/MPS/CPU with optimal placement

### 🔍 Advanced Debugging

- **Intermediate Steps**: Optional display of:
  - Retrieved document context
  - LegalBERT legal analysis
  - Final refined response
- **System Information**: Device configuration and memory usage
- **Error Handling**: Graceful fallbacks and user-friendly error messages

### 🎛️ Customizable Settings

- **Model Configuration**: Automatic fallback from LegalBERT to DistilBERT
- **Retrieval Parameters**: Configurable similarity search (default: k=3)
- **Display Options**: Toggle intermediate step visualization
- **Cache Control**: Manual cache clearing and performance reset

## 🚀 Quick Start Guide

### 📋 Prerequisites

1. **Ollama Service** running locally on port 11434
2. **Required Models** installed:
   - `nomic-embed-text` (embeddings)
   - `llama3.2:3b` (language generation)
3. **Pre-built Vector Store** in `legal_documents/` directory

### 🛠️ Installation Steps

#### Step 1: Setup Ollama

```bash
# Start Ollama service (if not already running)
ollama serve

# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2:3b

# Verify models are available
ollama list
```

#### Step 2: Install Python Dependencies

```bash
# Navigate to the project directory
cd "/Users/quest/dev/agents/Langchain-and-Ollama/17.2 RAG-Chat with Kenyan Constitution v2"

# Install all required packages
pip install -r requirements.txt
```

#### Step 3: Verify Vector Store

```bash
# Check that these files exist:
ls legal_documents/
# Should show: index.faiss, index.pkl
```

#### Step 4: Launch Application

```bash
# Start the Streamlit app
streamlit run app.py

# App will be available at: http://localhost:8501
```

## 🎯 Usage Examples

### Basic Queries

```
- "What does the Constitution say about sovereignty of the people?"
- "What are the fundamental rights and freedoms?"
- "How is the government structured according to the Constitution?"
- "What does the Constitution say about citizenship?"
- "What are the duties and responsibilities of citizens?"
```

### Advanced Features Usage

#### Enable Intermediate Steps

1. Check "Show intermediate steps" in the sidebar
2. Ask any question
3. Expand "🔍 Intermediate Steps" to see:
   - Retrieved context from Constitution
   - LegalBERT legal analysis
   - Processing pipeline details

#### Monitor Performance

1. Click "📊 Show Performance Stats" in sidebar
2. View metrics:
   - Total queries processed
   - Average response time
   - Cache hit rate
   - Cache size

#### Check System Information

1. Click "🔧 Show Device Info" in sidebar
2. View configuration:
   - Active device (CPU/CUDA/MPS)
   - Model information
   - Memory usage (if GPU)

## 🔧 Configuration Options

### Model Settings

```python
# Default configurations (can be customized in app.py)
LEGAL_BERT_MODEL = "nlpaueb/legal-bert-base-uncased"
FALLBACK_MODEL = "distilbert-base-uncased-distilled-squad"
EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3.2:3b"
RETRIEVAL_K = 3  # Number of documents to retrieve
```

### Device Preferences

```python
# Auto-detection priority:
# 1. CUDA (if available)
# 2. MPS (Apple Silicon, if available)
# 3. CPU (fallback)
```

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 🔴 Ollama Connection Error

**Problem**: `Connection refused` or `Ollama not found`

```bash
# Solution:
ollama serve  # Start Ollama service
# Wait for "Ollama server running" message
```

#### 🔴 Model Not Found

**Problem**: `Model 'llama3.2:3b' not found`

```bash
# Solution:
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

#### 🔴 Vector Store Error

**Problem**: `FAISS index not found`

```bash
# Solution: Verify these files exist:
ls legal_documents/index.faiss
ls legal_documents/index.pkl
# If missing, run the notebook first to generate the vector store
```

#### 🔴 Memory Issues

**Problem**: Out of memory or slow performance

```python
# Solutions:
# 1. Clear cache in sidebar
# 2. Restart the app
# 3. Use CPU mode if GPU memory is limited
```

#### 🔴 Package Installation Issues

```bash
# Create fresh environment:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 📊 Performance Optimization Tips

### 🚀 Speed Improvements

1. **Use GPU**: Ensure CUDA or MPS is available for faster processing
2. **Cache Utilization**: Repeated questions will be served from cache
3. **Model Management**: LegalBERT automatically falls back to smaller models if needed

### 💾 Memory Management

1. **Cache Clearing**: Use sidebar button to free memory
2. **Session Restart**: Refresh browser if app becomes sluggish
3. **Device Selection**: CPU mode uses less memory but is slower

### 📈 Monitoring Tools

- **Response Times**: Track in performance stats
- **Cache Efficiency**: Monitor hit rates
- **System Resources**: Check device information

## 🔒 Security & Privacy

### Data Handling

- **Local Processing**: All data stays on your machine
- **No External APIs**: Uses local Ollama models only
- **Session Storage**: Chat history cleared on browser refresh

### Model Security

- **Trusted Sources**: Models from Hugging Face and Ollama
- **Local Inference**: No data sent to external services
- **Fallback Safety**: Automatic model fallbacks prevent crashes

## 🤝 Contributing

### Adding Features

1. Modify `app.py` for UI changes
2. Update `requirements.txt` for new dependencies
3. Test with existing Constitution dataset
4. Update this documentation

### Custom Models

1. Replace model names in initialization functions
2. Ensure compatibility with LangChain interfaces
3. Test performance with different configurations

## 📞 Support

### Getting Help

1. Check this documentation first
2. Verify all prerequisites are met
3. Test with simple queries before complex ones
4. Monitor performance stats for bottlenecks

### Expected Behavior

- **First Query**: May take 10-30 seconds (model loading)
- **Subsequent Queries**: 2-10 seconds (cached components)
- **Error Recovery**: Automatic fallbacks and user notifications

---

**Note**: This application provides AI-generated analysis for educational purposes. Always consult qualified legal professionals for authoritative legal advice.
