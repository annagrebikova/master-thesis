"""
Unit tests for the Educational Assistant components
"""

import os
import sys

# Add parent directory to path so we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test document ingestion
def test_document_ingestion():
    print("\n" + "="*60)
    print("TEST 1: Document Ingestion")
    print("="*60)
    
    from src.utils.document_ingestion import DocumentIngester
    
    ingester = DocumentIngester()
    
    # Test TXT file ingestion
    file_path = "examples/lecture_materials/machine_learning_intro.txt"
    doc = ingester.ingest_document(file_path)
    
    assert 'content' in doc, "Document should have content"
    assert 'metadata' in doc, "Document should have metadata"
    assert len(doc['content']) > 0, "Content should not be empty"
    assert doc['metadata']['source'] == 'machine_learning_intro.txt'
    
    print(f"✓ Successfully ingested document")
    print(f"  - Source: {doc['metadata']['source']}")
    print(f"  - Size: {doc['metadata']['file_size']} bytes")
    print(f"  - Content length: {len(doc['content'])} characters")
    print(f"  - First 100 chars: {doc['content'][:100]}...")
    
    return True


def test_text_chunking():
    print("\n" + "="*60)
    print("TEST 2: Text Chunking")
    print("="*60)
    
    from src.utils.text_chunker import TextChunker
    from src.utils.document_ingestion import DocumentIngester
    
    ingester = DocumentIngester()
    chunker = TextChunker(chunk_size=500, chunk_overlap=100)
    
    file_path = "examples/lecture_materials/machine_learning_intro.txt"
    doc = ingester.ingest_document(file_path)
    
    chunks = chunker.chunk_text(doc['content'], doc['metadata'])
    
    assert len(chunks) > 0, "Should create at least one chunk"
    assert all('content' in c for c in chunks), "All chunks should have content"
    assert all('metadata' in c for c in chunks), "All chunks should have metadata"
    
    print(f"✓ Successfully chunked document")
    print(f"  - Number of chunks: {len(chunks)}")
    print(f"  - First chunk length: {len(chunks[0]['content'])} characters")
    print(f"  - Chunk 0 metadata: {chunks[0]['metadata']}")
    
    # Test chunk_documents
    docs = [doc]
    all_chunks = chunker.chunk_documents(docs)
    assert len(all_chunks) == len(chunks), "chunk_documents should produce same result"
    
    print(f"✓ chunk_documents() works correctly")
    
    return True


def test_cli_help():
    print("\n" + "="*60)
    print("TEST 3: CLI Help")
    print("="*60)
    
    import subprocess
    
    result = subprocess.run(
        ['python3', 'main.py', '--help'],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )
    
    assert result.returncode == 0, "CLI help should exit successfully"
    assert 'ingest' in result.stdout, "Help should mention ingest command"
    assert 'ask' in result.stdout, "Help should mention ask command"
    assert 'interactive' in result.stdout, "Help should mention interactive command"
    
    print(f"✓ CLI help works correctly")
    print(f"  Available commands: ingest, ask, interactive")
    
    return True


def test_module_imports():
    print("\n" + "="*60)
    print("TEST 4: Module Imports")
    print("="*60)
    
    try:
        from src.utils.document_ingestion import DocumentIngester
        print("✓ DocumentIngester imported")
        
        from src.utils.text_chunker import TextChunker
        print("✓ TextChunker imported")
        
        from src.rag.vector_store import VectorStore
        print("✓ VectorStore imported")
        
        from src.agents.retriever_agent import RetrieverAgent
        print("✓ RetrieverAgent imported")
        
        from src.agents.explainer_agent import ExplainerAgent
        print("✓ ExplainerAgent imported")
        
        from src.agents.feedback_handler_agent import FeedbackHandlerAgent
        print("✓ FeedbackHandlerAgent imported")
        
        from src.educational_assistant import EducationalAssistant
        print("✓ EducationalAssistant imported")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_supported_formats():
    print("\n" + "="*60)
    print("TEST 5: Supported Formats")
    print("="*60)
    
    from src.utils.document_ingestion import DocumentIngester
    
    ingester = DocumentIngester()
    expected_formats = ['.pdf', '.docx', '.pptx', '.txt']
    
    assert ingester.supported_formats == expected_formats, \
        f"Expected {expected_formats}, got {ingester.supported_formats}"
    
    print(f"✓ Supported formats: {', '.join(ingester.supported_formats)}")
    
    return True


def main():
    print("\n" + "="*70)
    print(" EDUCATIONAL ASSISTANT - BASIC TESTS")
    print("="*70)
    print("\nThese tests validate basic functionality without requiring API keys")
    
    tests = [
        ("Module Imports", test_module_imports),
        ("Document Ingestion", test_document_ingestion),
        ("Text Chunking", test_text_chunking),
        ("Supported Formats", test_supported_formats),
        ("CLI Help", test_cli_help),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"✗ {test_name} failed")
        except Exception as e:
            failed += 1
            print(f"\n✗ {test_name} failed with error:")
            print(f"  {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    print(f"Total tests: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
