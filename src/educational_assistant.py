"""
Multi-Agent Educational Assistant
Main orchestrator that coordinates all agents
"""

import os
from typing import Dict, List
from dotenv import load_dotenv

from src.utils.document_ingestion import DocumentIngester
from src.utils.text_chunker import TextChunker
from src.rag.vector_store import VectorStore
from src.agents.retriever_agent import RetrieverAgent
from src.agents.explainer_agent import ExplainerAgent
from src.agents.feedback_handler_agent import FeedbackHandlerAgent


class EducationalAssistant:
    """Main class that orchestrates the multi-agent educational assistant"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the educational assistant
        
        Args:
            chunk_size: Size of text chunks for vectorization
            chunk_overlap: Overlap between chunks
        """
        # Load environment variables
        load_dotenv()
        
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize components
        self.document_ingester = DocumentIngester()
        self.text_chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.vector_store = VectorStore()
        
        # Initialize agents (will be set up after documents are loaded)
        self.retriever_agent = None
        self.explainer_agent = None
        self.feedback_handler_agent = None
        
        self.is_initialized = False
    
    def ingest_documents(self, path: str) -> Dict:
        """
        Ingest documents from a file or directory
        
        Args:
            path: Path to file or directory
            
        Returns:
            Dictionary with ingestion statistics
        """
        print(f"Ingesting documents from: {path}")
        
        # Ingest documents
        if os.path.isfile(path):
            documents = [self.document_ingester.ingest_document(path)]
        elif os.path.isdir(path):
            documents = self.document_ingester.ingest_directory(path)
        else:
            raise ValueError(f"Path not found: {path}")
        
        if not documents:
            raise ValueError("No documents were successfully ingested")
        
        print(f"Ingested {len(documents)} document(s)")
        
        # Chunk documents
        chunks = self.text_chunker.chunk_documents(documents)
        print(f"Created {len(chunks)} chunks")
        
        # Create or update vector store
        if self.vector_store.vector_store is None:
            self.vector_store.create_vector_store(chunks)
        else:
            self.vector_store.add_documents(chunks)
        
        # Initialize agents if not already done
        if not self.is_initialized:
            self._initialize_agents()
        
        return {
            'num_documents': len(documents),
            'num_chunks': len(chunks),
            'status': 'success'
        }
    
    def _initialize_agents(self):
        """Initialize all agents"""
        self.retriever_agent = RetrieverAgent(self.vector_store)
        self.explainer_agent = ExplainerAgent()
        self.feedback_handler_agent = FeedbackHandlerAgent()
        self.is_initialized = True
        print("Agents initialized successfully")
    
    def ask(self, question: str, k: int = 4, include_follow_up: bool = False) -> Dict:
        """
        Ask a question and get an answer
        
        Args:
            question: User's question
            k: Number of relevant documents to retrieve
            include_follow_up: Whether to include follow-up questions
            
        Returns:
            Dictionary with answer and metadata
        """
        if not self.is_initialized:
            raise ValueError("System not initialized. Please ingest documents first.")
        
        # Step 1: Retrieve relevant context
        print(f"\n🔍 Retrieving relevant context...")
        retrieval_result = self.retriever_agent.retrieve(question, k=k)
        context = self.retriever_agent.get_context_string(retrieval_result)
        
        # Step 2: Generate explanation
        print(f"💡 Generating explanation...")
        if include_follow_up:
            explanation_result = self.explainer_agent.explain_with_follow_up(question, context)
        else:
            explanation_result = self.explainer_agent.explain(
                question, 
                context, 
                metadata=retrieval_result
            )
        
        # Combine results
        result = {
            'question': question,
            'answer': explanation_result.get('explanation', ''),
            'sources': [doc['metadata'].get('source', 'Unknown') 
                       for doc in retrieval_result['retrieved_documents']],
            'retrieval_info': {
                'num_sources': retrieval_result['num_results'],
                'refined_query': retrieval_result['refined_query']
            }
        }
        
        if include_follow_up:
            result['follow_up_questions'] = explanation_result.get('follow_up_questions', '')
        
        return result
    
    def provide_feedback(self, question: str, response: str, feedback: str, 
                        rating: int = None) -> Dict:
        """
        Provide feedback on a response
        
        Args:
            question: Original question
            response: System response
            feedback: User's feedback
            rating: Optional rating (1-5)
            
        Returns:
            Dictionary with feedback status
        """
        if not self.is_initialized:
            raise ValueError("System not initialized")
        
        return self.feedback_handler_agent.record_feedback(
            question, response, feedback, rating
        )
    
    def improve_based_on_feedback(self, question: str, previous_response: str, 
                                   feedback: str) -> Dict:
        """
        Generate an improved response based on feedback
        
        Args:
            question: Original question
            previous_response: Previous response
            feedback: User's feedback
            
        Returns:
            Dictionary with improved response
        """
        if not self.is_initialized:
            raise ValueError("System not initialized")
        
        # Retrieve context again
        retrieval_result = self.retriever_agent.retrieve(question, k=4)
        context = self.retriever_agent.get_context_string(retrieval_result)
        
        # Generate improved response
        return self.feedback_handler_agent.improve_response(
            question, previous_response, feedback, context
        )
    
    def get_feedback_summary(self) -> Dict:
        """Get summary of collected feedback"""
        if not self.is_initialized:
            raise ValueError("System not initialized")
        
        return self.feedback_handler_agent.get_feedback_summary()
    
    def save_vector_store(self, path: str = None):
        """Save the vector store to disk"""
        self.vector_store.save(path)
    
    def load_vector_store(self, path: str = None):
        """Load a previously saved vector store"""
        self.vector_store.load(path)
        if not self.is_initialized:
            self._initialize_agents()
