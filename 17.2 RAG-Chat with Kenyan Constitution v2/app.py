"""
Streamlit App for RAG Chat with Kenyan Constitution using Llama3.2

This app implements a RAG system that combines:
1. FAISS vector store for document retrieval
2. Llama3.2 for question answering
3. Performance monitoring
"""

import os
import streamlit as st
import warnings
import time
from typing import Optional, List, Any, Dict

# Suppress warnings
warnings.filterwarnings("ignore")
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Import required libraries
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class SimpleRAG:
    """
    Simple RAG pipeline using only Llama3.2.
    """
    
    def __init__(self, retriever, llama_model, prompt_template):
        self.retriever = retriever
        self.llama_model = llama_model
        self.prompt_template = prompt_template
        self.performance_stats = {"calls": 0, "avg_time": 0}
        
        # Create the RAG chain
        self.rag_chain = (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | self.prompt_template
            | self.llama_model
            | StrOutputParser()
        )
    
    def _format_docs(self, docs) -> str:
        """Format retrieved documents for processing."""
        return '\n\n'.join([doc.page_content for doc in docs])
    
    def query(self, question: str, return_intermediate=False) -> dict:
        """Process a query through the RAG pipeline with performance tracking."""
        start_time = time.time()
        self.performance_stats["calls"] += 1
        
        try:
            # Get the response from the RAG chain
            response = self.rag_chain.invoke(question)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Update performance stats
            total_time = self.performance_stats["avg_time"] * (self.performance_stats["calls"] - 1) + processing_time
            self.performance_stats["avg_time"] = total_time / self.performance_stats["calls"]
            
            result = {
                "question": question,
                "final_response": response,
                "processing_time": processing_time
            }
            
            if return_intermediate:
                # Get retrieved context for display
                docs = self.retriever.invoke(question)
                context = self._format_docs(docs)
                result.update({
                    "retrieved_context": context
                })
            
            return result
            
        except Exception as e:
            return {
                "question": question,
                "error": str(e),
                "processing_time": time.time() - start_time
            }
    
    def get_performance_stats(self):
        """Get performance statistics."""
        return {
            **self.performance_stats
        }


@st.cache_resource
def initialize_rag_system():
    """Initialize the RAG system with caching."""
    try:
        # Initialize embeddings
        embeddings = OllamaEmbeddings(model='nomic-embed-text', base_url='http://localhost:11434')
        
        # Load FAISS vector store
        db_name = "legal_documents"
        vector_store = FAISS.load_local(db_name, embeddings, allow_dangerous_deserialization=True)
        
        # Create retriever
        # retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 3})
        retriever = vector_store.as_retriever(search_type = 'similarity_score_threshold', 
                                      search_kwargs = {'k': 10, 'score_threshold': 0.1})
        
        # Initialize Llama model
        # llama_model = ChatOllama(model='llama3.2:3b', base_url='http://localhost:11434')
        llama_model = ChatOllama(model='deepseek-r1:8b', base_url='http://localhost:11434')
        
        # Create prompt template (based on the original pipeline from notebook)
        prompt_template_text = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know.
    Answer in bullet points. Make sure your answer is relevant to the question and it is answered from the context only.
    Question: {question} 
    Context: {context} 
    Answer:
"""
        
        prompt_template = ChatPromptTemplate.from_template(prompt_template_text)
        
        # Initialize simple RAG
        simple_rag = SimpleRAG(retriever, llama_model, prompt_template)
        
        return simple_rag, None
        
    except Exception as e:
        st.error(f"Failed to initialize RAG system: {e}")
        return None, None


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="🏛️ Kenyan Constitution RAG Chat",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title and header
    st.title("🏛️ RAG Chat with Kenyan Constitution")
    st.subheader("Llama3.2 Pipeline")
    
    # Sidebar for settings and information
    with st.sidebar:
        st.header("📋 System Information")
        
        # Initialize system
        if 'rag_system' not in st.session_state:
            with st.spinner("Initializing RAG system..."):
                rag_system, _ = initialize_rag_system()
                if rag_system:
                    st.session_state.rag_system = rag_system
                    st.success("✅ RAG system initialized!")
                else:
                    st.error("❌ Failed to initialize RAG system")
                    return
        
        # Performance statistics
        if st.button("📊 Show Performance Stats"):
            stats = st.session_state.rag_system.get_performance_stats()
            st.json(stats)
        
        # Settings
        st.header("⚙️ Settings")
        show_intermediate = st.checkbox("Show intermediate steps", value=False)
        
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant for questions about the Kenyan Constitution. I use Llama3.2 to provide clear responses based on the Constitution documents. How can I help you today?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if question := st.chat_input("Ask a question about the Kenyan Constitution..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Processing your question..."):
                result = st.session_state.rag_system.query(question, return_intermediate=show_intermediate)
                
                if "error" not in result:
                    # Display response
                    st.markdown("\n" + result["final_response"])
                    
                    # Show processing time
                    st.caption(f"⏱️ Processing time: {result['processing_time']:.2f} seconds")
                    
                    # Show intermediate steps if enabled
                    if show_intermediate:
                        with st.expander("🔍 Intermediate Steps"):
                            st.subheader("📄 Retrieved Context")
                            st.text_area("Context", result.get("retrieved_context", "")[:500] + "...", height=150)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": result["final_response"]})
                    
                else:
                    error_msg = f"❌ Error: {result['error']}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        **About this app:**
        - Uses Llama3.2 for question answering based on the Kenyan Constitution
        - Retrieves relevant sections from the Constitution documents
        - Provides performance monitoring for efficiency
        - Always consult qualified legal professionals for authoritative advice
        """
    )


if __name__ == "__main__":
    main()