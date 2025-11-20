#!/usr/bin/env python3
"""
Verify that all prerequisites for the RAG system are properly installed and configured.
Run this script before using the notebook to ensure everything is set up correctly.
"""
import os
import sys
from dotenv import load_dotenv

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"   {text}")

def check_python_version():
    """Check if Python version is 3.11+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print_success(f"Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python version: {version.major}.{version.minor}.{version.micro} (3.11+ required)")
        return False

def check_env_file():
    """Check if .env file exists"""
    if os.path.exists('.env'):
        print_success(".env file exists")
        load_dotenv()
        return True
    else:
        print_error(".env file not found")
        print_info("Run: cp .env.example .env")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    packages = {
        'psycopg2': 'psycopg2-binary',
        'pgvector': 'pgvector',
        'langchain': 'langchain',
        'langchain_community': 'langchain-community',
        'langchain_ollama': 'langchain-ollama',
        'dotenv': 'python-dotenv',
        'sklearn': 'scikit-learn',
        'numpy': 'numpy',
    }
    
    all_installed = True
    for module, package in packages.items():
        try:
            __import__(module)
            print_success(f"{package} installed")
        except ImportError:
            print_error(f"{package} not installed")
            print_info(f"Run: pip install {package}")
            all_installed = False
    
    return all_installed

def check_postgresql():
    """Check if PostgreSQL is running and accessible"""
    try:
        import psycopg2
        
        DB_NAME = os.getenv('DB_NAME', 'rag_db')
        DB_USER = os.getenv('DB_USER', os.getenv('USER'))
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '5432')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        
        conn = psycopg2.connect(
            dbname='postgres',  # Connect to default database first
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.close()
        print_success(f"PostgreSQL connection successful ({DB_HOST}:{DB_PORT})")
        return True
    except Exception as e:
        print_error(f"PostgreSQL connection failed: {str(e)[:60]}")
        print_info("Run: brew services start postgresql@18")
        return False

def check_database_exists():
    """Check if the rag_db database exists"""
    try:
        import psycopg2
        
        DB_NAME = os.getenv('DB_NAME', 'rag_db')
        DB_USER = os.getenv('DB_USER', os.getenv('USER'))
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '5432')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.close()
        print_success(f"Database '{DB_NAME}' exists")
        return True
    except Exception as e:
        print_error(f"Database '{DB_NAME}' not found")
        print_info("Run: python init_db.py")
        return False

def check_pgvector_extension():
    """Check if pgvector extension is installed"""
    try:
        import psycopg2
        
        DB_NAME = os.getenv('DB_NAME', 'rag_db')
        DB_USER = os.getenv('DB_USER', os.getenv('USER'))
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '5432')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector'")
            if cur.fetchone():
                print_success("pgvector extension enabled")
                result = True
            else:
                print_error("pgvector extension not enabled")
                print_info("Run: python init_db.py")
                result = False
        
        conn.close()
        return result
    except Exception as e:
        print_error(f"Cannot check pgvector extension: {str(e)[:60]}")
        return False

def check_chunks_table():
    """Check if chunks table exists"""
    try:
        import psycopg2
        
        DB_NAME = os.getenv('DB_NAME', 'rag_db')
        DB_USER = os.getenv('DB_USER', os.getenv('USER'))
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '5432')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM chunks")
            count = cur.fetchone()[0]
            print_success(f"chunks table exists ({count} chunks)")
        
        conn.close()
        return True
    except Exception as e:
        print_error(f"chunks table not found")
        print_info("Run: python init_db.py")
        return False

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        
        OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        
        response = requests.get(f'{OLLAMA_BASE_URL}/api/tags', timeout=2)
        if response.status_code == 200:
            print_success(f"Ollama is running ({OLLAMA_BASE_URL})")
            return True
        else:
            print_error("Ollama is not responding")
            print_info("Run: ollama serve")
            return False
    except Exception as e:
        print_error("Cannot connect to Ollama")
        print_info("Run: ollama serve")
        return False

def check_ollama_models():
    """Check if required Ollama models are installed"""
    try:
        import requests
        
        OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        OLLAMA_EMBED_MODEL = os.getenv('OLLAMA_EMBED_MODEL', 'nomic-embed-text')
        OLLAMA_LLM_MODEL = os.getenv('OLLAMA_LLM_MODEL', 'llama3.2:3b')
        
        response = requests.get(f'{OLLAMA_BASE_URL}/api/tags', timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [m['name'] for m in models]
            
            embed_found = any(OLLAMA_EMBED_MODEL in name for name in model_names)
            llm_found = any(OLLAMA_LLM_MODEL in name for name in model_names)
            
            if embed_found:
                print_success(f"Embedding model '{OLLAMA_EMBED_MODEL}' installed")
            else:
                print_error(f"Embedding model '{OLLAMA_EMBED_MODEL}' not found")
                print_info(f"Run: ollama pull {OLLAMA_EMBED_MODEL}")
            
            if llm_found:
                print_success(f"LLM model '{OLLAMA_LLM_MODEL}' installed")
            else:
                print_error(f"LLM model '{OLLAMA_LLM_MODEL}' not found")
                print_info(f"Run: ollama pull {OLLAMA_LLM_MODEL}")
            
            return embed_found and llm_found
        else:
            return False
    except Exception as e:
        print_error(f"Cannot check Ollama models: {str(e)[:60]}")
        return False

def main():
    print_header("RAG System Prerequisites Check")
    
    checks = {
        "Python Version": check_python_version,
        "Environment File": check_env_file,
        "Python Packages": check_python_packages,
        "PostgreSQL": check_postgresql,
        "Database": check_database_exists,
        "pgvector Extension": check_pgvector_extension,
        "chunks Table": check_chunks_table,
        "Ollama": check_ollama,
        "Ollama Models": check_ollama_models,
    }
    
    results = {}
    for name, check_func in checks.items():
        print(f"\n{name}:")
        results[name] = check_func()
    
    # Summary
    print_header("Summary")
    passed = sum(results.values())
    total = len(results)
    
    if passed == total:
        print_success(f"All checks passed! ({passed}/{total})")
        print_info("✨ You're ready to run the notebook!")
    else:
        print_warning(f"Some checks failed ({passed}/{total} passed)")
        print_info("📝 Please fix the issues above before running the notebook")
        print_info("📚 See QUICKSTART.md for detailed setup instructions")
    
    print()

if __name__ == "__main__":
    main()
