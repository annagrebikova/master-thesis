"""
Vector Store Module
Handles vectorization and FAISS-based retrieval
"""

import os
import pickle
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class VectorStore:
    """Manages document vectorization and retrieval using FAISS"""
    
    def __init__(self, embedding_model: str = "text-embedding-ada-002"):
        """
        Initialize vector store
        
        Args:
            embedding_model: OpenAI embedding model to use
        """
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vector_store = None
        self.store_path = "vector_store"
    
    def create_vector_store(self, chunks: List[Dict]) -> None:
        """
        Create FAISS vector store from document chunks
        
        Args:
            chunks: List of document chunks with 'content' and 'metadata' keys
        """
        if not chunks:
            raise ValueError("No chunks provided to create vector store")
        
        # Convert chunks to LangChain Document format
        documents = []
        for chunk in chunks:
            doc = Document(
                page_content=chunk['content'],
                metadata=chunk.get('metadata', {})
            )
            documents.append(doc)
        
        # Create FAISS vector store
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        print(f"Vector store created with {len(documents)} chunks")
    
    def add_documents(self, chunks: List[Dict]) -> None:
        """
        Add new documents to existing vector store
        
        Args:
            chunks: List of document chunks with 'content' and 'metadata' keys
        """
        if not self.vector_store:
            self.create_vector_store(chunks)
            return
        
        documents = []
        for chunk in chunks:
            doc = Document(
                page_content=chunk['content'],
                metadata=chunk.get('metadata', {})
            )
            documents.append(doc)
        
        self.vector_store.add_documents(documents)
        print(f"Added {len(documents)} chunks to vector store")
    
    def similarity_search(self, query: str, k: int = 4) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant document chunks with metadata
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please add documents first.")
        
        # Perform similarity search
        results = self.vector_store.similarity_search(query, k=k)
        
        # Format results
        formatted_results = []
        for doc in results:
            formatted_results.append({
                'content': doc.page_content,
                'metadata': doc.metadata
            })
        
        return formatted_results
    
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """
        Search for similar documents with relevance scores
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of tuples (document_dict, score)
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Please add documents first.")
        
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append(({
                'content': doc.page_content,
                'metadata': doc.metadata
            }, score))
        
        return formatted_results
    
    def save(self, path: str = None) -> None:
        """
        Save vector store to disk
        
        Args:
            path: Directory path to save the vector store
        """
        if not self.vector_store:
            raise ValueError("No vector store to save")
        
        save_path = path or self.store_path
        os.makedirs(save_path, exist_ok=True)
        
        # Save FAISS index
        self.vector_store.save_local(save_path)
        print(f"Vector store saved to {save_path}")
    
    def load(self, path: str = None) -> None:
        """
        Load vector store from disk
        
        Args:
            path: Directory path to load the vector store from
        """
        load_path = path or self.store_path
        
        if not os.path.exists(load_path):
            raise FileNotFoundError(f"Vector store not found at {load_path}")
        
        # Load FAISS index
        self.vector_store = FAISS.load_local(
            load_path, 
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"Vector store loaded from {load_path}")
