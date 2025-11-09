"""
Text Chunking Module
Handles splitting of documents into manageable chunks for vectorization
"""

from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    """Splits text into chunks with overlap for better context preservation"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize text chunker
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def chunk_text(self, text: str, metadata: dict = None) -> List[Dict]:
        """
        Split text into chunks
        
        Args:
            text: Text to split
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of dictionaries with 'content' and 'metadata' keys
        """
        if not text or not text.strip():
            return []
        
        chunks = self.text_splitter.split_text(text)
        
        result = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = metadata.copy() if metadata else {}
            chunk_metadata['chunk_id'] = i
            chunk_metadata['total_chunks'] = len(chunks)
            
            result.append({
                'content': chunk,
                'metadata': chunk_metadata
            })
        
        return result
    
    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Chunk multiple documents
        
        Args:
            documents: List of documents with 'content' and 'metadata' keys
            
        Returns:
            List of chunked documents
        """
        all_chunks = []
        for doc in documents:
            chunks = self.chunk_text(doc['content'], doc.get('metadata', {}))
            all_chunks.extend(chunks)
        
        return all_chunks
