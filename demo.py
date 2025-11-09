"""
Demo script showing the Educational Assistant capabilities
This demo runs without requiring OpenAI API keys
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.document_ingestion import DocumentIngester
from src.utils.text_chunker import TextChunker


def demo_document_processing():
    """Demonstrate document processing capabilities"""
    print("\n" + "="*70)
    print(" DEMO: Document Processing")
    print("="*70)
    
    # Initialize components
    ingester = DocumentIngester()
    chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
    
    print("\n📁 Step 1: Ingesting lecture materials...")
    print("-" * 70)
    
    # Ingest documents
    docs_dir = "examples/lecture_materials"
    documents = ingester.ingest_directory(docs_dir)
    
    print(f"✓ Ingested {len(documents)} document(s)")
    for doc in documents:
        print(f"  - {doc['metadata']['source']} ({doc['metadata']['file_size']} bytes)")
    
    print("\n📄 Step 2: Chunking documents...")
    print("-" * 70)
    
    chunks = chunker.chunk_documents(documents)
    
    print(f"✓ Created {len(chunks)} chunks")
    print(f"  - Chunk size: {chunker.chunk_size} characters")
    print(f"  - Chunk overlap: {chunker.chunk_overlap} characters")
    
    print("\n📊 Step 3: Sample chunk preview...")
    print("-" * 70)
    
    if chunks:
        sample_chunk = chunks[0]
        print(f"Chunk 0:")
        print(f"  Source: {sample_chunk['metadata']['source']}")
        print(f"  Length: {len(sample_chunk['content'])} characters")
        print(f"  Content preview:")
        print(f"  {sample_chunk['content'][:200]}...")
    
    return documents, chunks


def demo_system_overview():
    """Show system architecture and capabilities"""
    print("\n" + "="*70)
    print(" MULTI-AGENT EDUCATIONAL ASSISTANT SYSTEM")
    print("="*70)
    
    print("\n🎯 SYSTEM ARCHITECTURE")
    print("-" * 70)
    print("""
The system consists of three specialized agents:

1. 🔍 RETRIEVER AGENT
   - Finds relevant context from vectorized documents
   - Refines user queries for better retrieval
   - Uses FAISS vector store for similarity search
   - Returns top-k most relevant document chunks

2. 💡 EXPLAINER AGENT
   - Generates clear, educational explanations
   - Uses retrieved context to ground responses
   - Provides follow-up questions (optional)
   - Structures answers logically

3. 📝 FEEDBACK HANDLER AGENT
   - Collects and analyzes user feedback
   - Generates improved responses based on feedback
   - Maintains feedback history
   - Helps improve system over time
    """)
    
    print("\n📚 SUPPORTED DOCUMENT FORMATS")
    print("-" * 70)
    
    ingester = DocumentIngester()
    for fmt in ingester.supported_formats:
        print(f"  ✓ {fmt.upper()[1:]} files")
    
    print("\n🔧 RAG PIPELINE")
    print("-" * 70)
    print("""
1. Document Ingestion
   └─> Extract text from PDFs, DOCX, PPTX, TXT files

2. Text Chunking
   └─> Split documents into overlapping chunks
   
3. Vectorization
   └─> Convert chunks to embeddings using OpenAI
   
4. Vector Store
   └─> Store embeddings in FAISS for fast retrieval
   
5. Query Processing
   ├─> Retrieve relevant chunks via similarity search
   ├─> Generate explanation using LLM
   └─> Collect feedback and improve
    """)


def demo_cli_usage():
    """Show CLI usage examples"""
    print("\n" + "="*70)
    print(" CLI USAGE EXAMPLES")
    print("="*70)
    
    print("\n📥 INGESTING DOCUMENTS")
    print("-" * 70)
    print("""
# Ingest from a directory:
python main.py ingest --path examples/lecture_materials

# Ingest and save vector store:
python main.py ingest --path examples/lecture_materials --save vector_store
    """)
    
    print("\n❓ ASKING QUESTIONS")
    print("-" * 70)
    print("""
# Ask a question:
python main.py ask --path examples/lecture_materials \\
    --question "What is machine learning?"

# With follow-up questions:
python main.py ask --path examples/lecture_materials \\
    --question "Explain neural networks" --follow-up

# Using saved vector store:
python main.py ask --load vector_store \\
    --question "What is supervised learning?"
    """)
    
    print("\n💬 INTERACTIVE MODE")
    print("-" * 70)
    print("""
# Start interactive session:
python main.py interactive --path examples/lecture_materials

# Or with saved vector store:
python main.py interactive --load vector_store

In interactive mode:
  - Type your questions and press Enter
  - Type 'feedback' to provide feedback on the last answer
  - Type 'quit' or 'exit' to stop
    """)


def demo_python_api():
    """Show Python API usage examples"""
    print("\n" + "="*70)
    print(" PYTHON API USAGE")
    print("="*70)
    
    print("""
from src.educational_assistant import EducationalAssistant

# Initialize
assistant = EducationalAssistant()

# Ingest documents
result = assistant.ingest_documents("examples/lecture_materials")
print(f"Ingested {result['num_documents']} documents")

# Ask a question
answer = assistant.ask("What is machine learning?")
print(answer['answer'])
print(f"Sources: {answer['sources']}")

# With follow-up questions
result = assistant.ask("Explain neural networks", include_follow_up=True)
print(result['answer'])
print(result['follow_up_questions'])

# Provide feedback
assistant.provide_feedback(
    question="What is machine learning?",
    response=answer['answer'],
    feedback="Great! Could you add more examples?",
    rating=4
)

# Get improved response
improved = assistant.improve_based_on_feedback(
    question="What is machine learning?",
    previous_response=answer['answer'],
    feedback="Add more real-world examples"
)
print(improved['improved_response'])

# Save/load vector store
assistant.save_vector_store("vector_store")
assistant.load_vector_store("vector_store")
    """)


def main():
    print("\n" + "="*70)
    print(" 🎓 EDUCATIONAL ASSISTANT DEMONSTRATION")
    print("="*70)
    print("\nThis demo showcases the multi-agent RAG system capabilities")
    
    # Run demos
    demo_system_overview()
    demo_document_processing()
    demo_cli_usage()
    demo_python_api()
    
    print("\n" + "="*70)
    print(" 📋 NEXT STEPS")
    print("="*70)
    print("""
To use the system with actual AI responses:

1. Set up your OpenAI API key:
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY

2. Run the basic tests:
   python tests/test_basic.py

3. Try the CLI:
   python main.py interactive --path examples/lecture_materials

4. Check the full documentation:
   See README.md for detailed usage instructions

For more examples, see: examples/example_usage.py
    """)
    
    print("\n✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
