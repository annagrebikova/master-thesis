"""
Retriever Agent
Responsible for finding relevant context from the vector store
"""

from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class RetrieverAgent:
    """Agent responsible for retrieving relevant context from documents"""
    
    def __init__(self, vector_store, llm_model: str = "gpt-3.5-turbo"):
        """
        Initialize retriever agent
        
        Args:
            vector_store: VectorStore instance for document retrieval
            llm_model: OpenAI model to use for query refinement
        """
        self.vector_store = vector_store
        self.llm = ChatOpenAI(model=llm_model, temperature=0)
        
        # Prompt for query refinement
        self.query_refinement_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant that refines user queries to improve document retrieval. "
                      "Make the query more specific and focused while preserving the user's intent."),
            ("user", "Original query: {query}\n\nProvide a refined version of this query for better document search.")
        ])
    
    def refine_query(self, query: str) -> str:
        """
        Refine user query for better retrieval
        
        Args:
            query: Original user query
            
        Returns:
            Refined query string
        """
        try:
            chain = self.query_refinement_prompt | self.llm
            response = chain.invoke({"query": query})
            return response.content.strip()
        except Exception as e:
            print(f"Query refinement failed: {e}. Using original query.")
            return query
    
    def retrieve(self, query: str, k: int = 4, refine: bool = True) -> Dict:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query
            k: Number of documents to retrieve
            refine: Whether to refine the query before retrieval
            
        Returns:
            Dictionary with original query, refined query, and retrieved documents
        """
        # Optionally refine query
        refined_query = self.refine_query(query) if refine else query
        
        # Retrieve documents
        results = self.vector_store.similarity_search_with_score(refined_query, k=k)
        
        # Format retrieved documents
        retrieved_docs = []
        for doc, score in results:
            retrieved_docs.append({
                'content': doc['content'],
                'metadata': doc['metadata'],
                'relevance_score': float(score)
            })
        
        return {
            'original_query': query,
            'refined_query': refined_query,
            'retrieved_documents': retrieved_docs,
            'num_results': len(retrieved_docs)
        }
    
    def get_context_string(self, retrieval_result: Dict) -> str:
        """
        Convert retrieved documents to a context string
        
        Args:
            retrieval_result: Result from retrieve() method
            
        Returns:
            Formatted context string
        """
        docs = retrieval_result['retrieved_documents']
        context_parts = []
        
        for i, doc in enumerate(docs, 1):
            source = doc['metadata'].get('source', 'Unknown')
            content = doc['content']
            context_parts.append(f"[Source {i}: {source}]\n{content}\n")
        
        return "\n".join(context_parts)
