"""
Initialize PostgreSQL 18+ database with pgvector extension and chunks table.
Run this script before using the RAG notebook.
"""
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'rag_db')
DB_USER = os.getenv('DB_USER', os.getenv('USER'))
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f'CREATE DATABASE {DB_NAME}')
            print(f"✅ Database '{DB_NAME}' created successfully")
        else:
            print(f"ℹ️  Database '{DB_NAME}' already exists")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        raise

def setup_schema():
    """Create pgvector extension and chunks table"""
    try:
        # Connect to the target database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()
        
        # Create pgvector extension
        cur.execute('CREATE EXTENSION IF NOT EXISTS vector')
        print("✅ pgvector extension created/verified")
        
        # Create chunks table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                embedding vector(768) NOT NULL,
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ chunks table created/verified")
        
        # Create index for faster similarity search
        cur.execute('''
            CREATE INDEX IF NOT EXISTS chunks_embedding_idx 
            ON chunks USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100)
        ''')
        print("✅ Vector similarity index created/verified")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"\n🎉 Database setup complete!")
        print(f"   Database: {DB_NAME}")
        print(f"   Host: {DB_HOST}:{DB_PORT}")
        
    except Exception as e:
        print(f"❌ Error setting up schema: {e}")
        raise

if __name__ == "__main__":
    print("🔧 Initializing PostgreSQL database for RAG system...")
    print(f"   Target database: {DB_NAME}")
    print(f"   PostgreSQL host: {DB_HOST}:{DB_PORT}")
    print()
    
    create_database()
    setup_schema()
    
    print("\n📝 Next steps:")
    print("   1. Copy .env.example to .env and update with your credentials")
    print("   2. Run the RAG notebook to ingest documents")
    print("   3. Query your documents using natural language")
