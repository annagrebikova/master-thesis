# Multi-Agent Educational Assistant

A Python-based multi-agent educational assistant using LangChain and FAISS for Retrieval-Augmented Generation (RAG). This system ingests lecture materials (PDF, DOCX, PPTX), chunks and vectorizes them, then answers user queries with grounded context and metadata.

## Features

### 🎯 Multi-Agent Architecture
- **Retriever Agent**: Finds relevant context from vectorized documents using FAISS
- **Explainer Agent**: Generates clear, educational explanations based on retrieved context
- **Feedback Handler Agent**: Processes user feedback and improves responses

### 📚 Document Processing
- Supports PDF, DOCX, and PPTX file formats
- Intelligent text chunking with overlap for context preservation
- Automatic metadata extraction and tracking

### 🔍 RAG System
- FAISS vector store for efficient similarity search
- OpenAI embeddings for document vectorization
- Query refinement for improved retrieval
- Relevance scoring for retrieved documents

### 💬 User Interaction
- Command-line interface (CLI)
- Interactive mode for continuous Q&A
- Follow-up question suggestions
- Feedback collection and response improvement

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/annagrebikova/master-thesis.git
cd master-thesis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Command-Line Interface

#### 1. Ingest Documents

Ingest documents from a directory:
```bash
python main.py ingest --path examples/lecture_materials
```

Ingest and save vector store:
```bash
python main.py ingest --path examples/lecture_materials --save vector_store
```

#### 2. Ask Questions

Ask a question about ingested documents:
```bash
python main.py ask --path examples/lecture_materials --question "What is machine learning?"
```

Ask with follow-up questions:
```bash
python main.py ask --path examples/lecture_materials --question "Explain neural networks" --follow-up
```

Use a saved vector store:
```bash
python main.py ask --load vector_store --question "What is supervised learning?"
```

#### 3. Interactive Mode

Start interactive Q&A session:
```bash
python main.py interactive --path examples/lecture_materials
```

Or with a saved vector store:
```bash
python main.py interactive --load vector_store
```

In interactive mode:
- Type your questions and press Enter
- Type `feedback` to provide feedback on the last answer
- Type `quit` or `exit` to stop

### Python API

```python
from src.educational_assistant import EducationalAssistant

# Initialize assistant
assistant = EducationalAssistant()

# Ingest documents
result = assistant.ingest_documents("path/to/documents")

# Ask a question
answer = assistant.ask("What is machine learning?")
print(answer['answer'])
print(f"Sources: {answer['sources']}")

# Ask with follow-up questions
result = assistant.ask("Explain neural networks", include_follow_up=True)
print(result['answer'])
print(result['follow_up_questions'])

# Provide feedback
assistant.provide_feedback(
    question="What is machine learning?",
    response=answer['answer'],
    feedback="Great explanation! Could you add more examples?",
    rating=4
)

# Get improved response based on feedback
improved = assistant.improve_based_on_feedback(
    question="What is machine learning?",
    previous_response=answer['answer'],
    feedback="Add more real-world examples"
)
print(improved['improved_response'])

# Save vector store for reuse
assistant.save_vector_store("vector_store")

# Load existing vector store
assistant.load_vector_store("vector_store")
```

## Project Structure

```
master-thesis/
├── src/
│   ├── agents/
│   │   ├── retriever_agent.py       # Retrieves relevant context
│   │   ├── explainer_agent.py       # Generates explanations
│   │   └── feedback_handler_agent.py # Handles feedback
│   ├── rag/
│   │   └── vector_store.py          # FAISS vector store
│   ├── utils/
│   │   ├── document_ingestion.py    # Document loading
│   │   └── text_chunker.py          # Text chunking
│   └── educational_assistant.py     # Main orchestrator
├── examples/
│   ├── lecture_materials/           # Sample documents
│   └── example_usage.py             # Usage examples
├── main.py                          # CLI interface
├── requirements.txt                 # Dependencies
├── .env.example                     # Environment template
└── README.md                        # This file
```

## How It Works

### 1. Document Ingestion
The system processes documents through several steps:
- **Loading**: Extracts text from PDF, DOCX, and PPTX files
- **Chunking**: Splits text into overlapping chunks (default: 1000 chars with 200 char overlap)
- **Metadata**: Attaches source information to each chunk

### 2. Vectorization
- Chunks are converted to embeddings using OpenAI's `text-embedding-ada-002` model
- Embeddings are stored in a FAISS vector database for efficient similarity search

### 3. Query Processing
When a user asks a question:

**Retriever Agent**:
- Refines the query for better retrieval (optional)
- Performs similarity search in the vector store
- Returns top-k most relevant chunks with scores

**Explainer Agent**:
- Takes the retrieved context and user question
- Generates a clear, educational explanation
- Optionally suggests follow-up questions

**Feedback Handler Agent**:
- Collects and analyzes user feedback
- Generates improved responses based on feedback
- Maintains feedback history for system improvement

## Configuration

### Chunking Parameters

Adjust in `EducationalAssistant` initialization:
```python
assistant = EducationalAssistant(
    chunk_size=1000,      # Characters per chunk
    chunk_overlap=200     # Overlap between chunks
)
```

### Retrieval Parameters

Adjust when asking questions:
```python
answer = assistant.ask(
    "Your question",
    k=4  # Number of relevant chunks to retrieve
)
```

### Agent Models

Agents use different LLM configurations optimized for their tasks:
- Retriever Agent: GPT-3.5-turbo (temperature=0) for precise query refinement
- Explainer Agent: GPT-3.5-turbo (temperature=0.7) for creative explanations
- Feedback Handler: GPT-3.5-turbo (temperature=0.3) for balanced analysis

## Examples

See `examples/example_usage.py` for comprehensive examples:

```bash
python examples/example_usage.py
```

This demonstrates:
- Basic document ingestion and Q&A
- Follow-up question generation
- Feedback handling and response improvement
- Saving and loading vector stores

## Dependencies

Core dependencies:
- `langchain`: LLM framework and RAG utilities
- `langchain-openai`: OpenAI integration
- `faiss-cpu`: Vector similarity search
- `pypdf`: PDF processing
- `python-docx`: DOCX processing
- `python-pptx`: PPTX processing
- `openai`: OpenAI API client

See `requirements.txt` for complete list.

## Limitations

- Requires OpenAI API key (paid service)
- Quality depends on source document quality and structure
- Large document collections may require significant processing time
- Context window limitations apply to LLM responses

## Future Enhancements

Potential improvements:
- Support for additional document formats (TXT, Markdown, etc.)
- Multiple embedding model options
- Conversation history tracking
- Fine-tuning capabilities
- Web interface
- Multi-language support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with LangChain framework
- Uses FAISS for efficient vector search
- Powered by OpenAI's language models

---

For questions or issues, please open an issue on GitHub.