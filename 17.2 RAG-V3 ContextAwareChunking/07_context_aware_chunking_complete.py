"""Context-Aware Chunking - Semantic boundaries using embedding similarity"""
import os
import psycopg2
from pgvector.psycopg2 import register_vector
import numpy as np
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Ollama configuration
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_EMBED_MODEL = os.getenv('OLLAMA_EMBED_MODEL', 'nomic-embed-text')
OLLAMA_LLM_MODEL = os.getenv('OLLAMA_LLM_MODEL', 'qwen2.5:7b')

# Database connection
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME', 'rag_db'),
    user=os.getenv('DB_USER', os.getenv('USER')),
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432')
)
register_vector(conn)

def get_embedding(text: str) -> list[float]:
    """Get embedding for text using Ollama"""
    response = requests.post(
        f'{OLLAMA_BASE_URL}/api/embeddings',
        json={
            'model': OLLAMA_EMBED_MODEL,
            'prompt': text
        }
    )
    if response.status_code != 200:
        raise Exception(f"Ollama embedding failed: {response.text}")
    return response.json()['embedding']

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def semantic_chunk(text: str, similarity_threshold=0.8) -> list[str]:
    """Chunk based on semantic similarity, not fixed size"""
    sentences = text.split('. ')  # Simple sentence split
    
    # Filter out empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= 1:
        return sentences
    
    sentence_embeddings = [get_embedding(s) for s in sentences]

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(len(sentences) - 1):
        similarity = cosine_similarity(sentence_embeddings[i], sentence_embeddings[i+1])

        if similarity > similarity_threshold:  # Same topic
            current_chunk.append(sentences[i+1])
        else:  # Topic boundary detected
            chunks.append('. '.join(current_chunk))
            current_chunk = [sentences[i+1]]

    chunks.append('. '.join(current_chunk))
    return chunks

def ingest_document(text: str):
    """Ingest a document by chunking it and storing in the database"""
    chunks = semantic_chunk(text)  # Semantic chunking
    with conn.cursor() as cur:
        for chunk in chunks:
            embedding = get_embedding(chunk)
            cur.execute('INSERT INTO chunks (content, embedding) VALUES (%s, %s)',
                       (chunk, embedding))
    conn.commit()
    print(f"Ingested {len(chunks)} chunks into the database")

def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for relevant chunks"""
    with conn.cursor() as cur:
        query_embedding = get_embedding(query)
        cur.execute('SELECT content FROM chunks ORDER BY embedding <=> %s::vector LIMIT 3',
                   (query_embedding,))
        results = cur.fetchall()
        if not results:
            return "No relevant information found in the knowledge base."
        return "\n\n".join([row[0] for row in results])

def answer_question(question: str) -> str:
    """Answer a question using RAG"""
    # Get relevant context
    context = search_knowledge_base(question)
    
    # Create prompt with context
    prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""
    
    # Get answer from Ollama
    response = requests.post(
        f'{OLLAMA_BASE_URL}/api/generate',
        json={
            'model': OLLAMA_LLM_MODEL,
            'prompt': prompt,
            'stream': False
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"Ollama generation failed: {response.text}")
    
    return response.json()['response']

# Example usage
if __name__ == "__main__":
    # Check if we have data in the database
    with conn.cursor() as cur:
        cur.execute('SELECT COUNT(*) FROM chunks')
        count = cur.fetchone()[0]
        print(f"Current chunks in database: {count}")
    
    # If no data, ingest a sample document
    if count == 0:
        print("\nIngesting sample document...")
        sample_text = """
        Deep learning is a subset of machine learning that uses neural networks with multiple layers.
        These networks can learn hierarchical representations of data.
        Neural networks are inspired by the structure of the human brain.
        They consist of interconnected nodes called neurons that process information.
        Deep learning has revolutionized computer vision and natural language processing.
        Applications include image recognition, speech synthesis, and language translation.
        Training deep learning models requires large amounts of data and computational power.
        """
        ingest_document(sample_text)
    
    # Query the knowledge base
    print("\nQuerying: 'What is deep learning?'")
    answer = answer_question("What is deep learning?")
    print(f"\nAnswer: {answer}")
    
    # Clean up
    conn.close()
