#!/usr/bin/env python3
"""
Diagnostic script to identify missing chunks in the embeddings table
"""
import psycopg2
import os
import pickle
from pathlib import Path

# Database configuration
DB_NAME = 'legalrag_v4_db'
DB_USER = os.getenv('USER')
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_PASSWORD = ''

print("🔍 Investigating discrepancy between expected (831) and actual (814) chunks...\n")

# Connect to database
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

# Get all embedded chunk_ids from database
with conn.cursor() as cur:
    cur.execute("SELECT chunk_id FROM embeddings ORDER BY chunk_id")
    embedded_ids = {row[0] for row in cur.fetchall()}

conn.close()

# Load final_chunks from the notebook kernel (if available)
# We'll need to check if we can load this from a pickle file or CSV
chunks_dir = Path("pipeline_storage/09_chunks")
if chunks_dir.exists():
    chunk_files = list(chunks_dir.glob("*_final_chunks.pkl"))
    if chunk_files:
        print(f"📁 Found chunk files: {[f.name for f in chunk_files]}\n")
        
        # Load all chunks
        all_chunks = []
        for chunk_file in chunk_files:
            with open(chunk_file, 'rb') as f:
                chunks = pickle.load(f)
                all_chunks.extend(chunks)
        
        print(f"📊 Loaded {len(all_chunks)} chunks from disk\n")
        
        # Generate expected chunk_ids
        expected_ids = []
        chunk_id_mapping = {}
        
        for chunk in all_chunks:
            version_id = chunk.metadata.get('version_id', 'unknown')
            chunk_num = chunk.metadata.get('chunk_num', 0)
            chunk_id = f"{version_id}_{chunk_num}"
            expected_ids.append(chunk_id)
            chunk_id_mapping[chunk_id] = chunk
        
        expected_set = set(expected_ids)
        
        # Find missing and duplicate chunks
        missing_ids = expected_set - embedded_ids
        duplicate_expected = [id for id in expected_ids if expected_ids.count(id) > 1]
        
        print(f"📊 Summary:")
        print(f"   Expected chunks (from disk): {len(expected_ids)}")
        print(f"   Unique expected chunk IDs: {len(expected_set)}")
        print(f"   Embedded in database: {len(embedded_ids)}")
        print(f"   Missing from database: {len(missing_ids)}")
        print(f"   Duplicate IDs in expected: {len(set(duplicate_expected))}")
        
        if duplicate_expected:
            print(f"\n⚠️  Found {len(set(duplicate_expected))} duplicate chunk IDs:")
            for dup_id in sorted(set(duplicate_expected))[:10]:
                count = expected_ids.count(dup_id)
                print(f"   - {dup_id}: appears {count} times")
            if len(set(duplicate_expected)) > 10:
                print(f"   ... and {len(set(duplicate_expected)) - 10} more")
        
        if missing_ids:
            print(f"\n❌ Missing chunk IDs ({len(missing_ids)}):")
            for miss_id in sorted(missing_ids)[:20]:
                chunk = chunk_id_mapping.get(miss_id)
                if chunk:
                    preview = chunk.page_content[:80].replace('\n', ' ')
                    print(f"   - {miss_id}: {preview}...")
            if len(missing_ids) > 20:
                print(f"   ... and {len(missing_ids) - 20} more")
        
        # Check if duplicates explain the discrepancy
        if len(duplicate_expected) > 0:
            unique_expected_count = len(expected_set)
            discrepancy = len(expected_ids) - unique_expected_count
            print(f"\n💡 Analysis:")
            print(f"   Duplicates explain {discrepancy} of the difference")
            print(f"   Expected unique chunks: {unique_expected_count}")
            print(f"   Actual embedded: {len(embedded_ids)}")
            remaining_gap = unique_expected_count - len(embedded_ids)
            if remaining_gap > 0:
                print(f"   ⚠️  Still {remaining_gap} chunks legitimately missing")
            elif remaining_gap == 0:
                print(f"   ✅ All unique chunks are accounted for!")
            else:
                print(f"   ⚠️  Database has {abs(remaining_gap)} more chunks than expected")
    else:
        print("❌ No chunk pickle files found in pipeline_storage/09_chunks/")
else:
    print("❌ Chunks directory not found: pipeline_storage/09_chunks/")
    print("   The script needs access to the chunk files to identify missing chunks.")
