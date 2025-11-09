"""
Explainer Agent
Responsible for generating clear, educational explanations based on retrieved context
"""

from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


class ExplainerAgent:
    """Agent responsible for providing clear educational explanations"""
    
    def __init__(self, llm_model: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """
        Initialize explainer agent
        
        Args:
            llm_model: OpenAI model to use
            temperature: Creativity parameter (0-1)
        """
        self.llm = ChatOpenAI(model=llm_model, temperature=temperature)
        
        # Prompt template for generating explanations
        self.explanation_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an expert educational assistant. Your role is to provide clear, accurate, and helpful "
             "explanations based on the provided lecture materials. Follow these guidelines:\n"
             "1. Base your answer primarily on the provided context\n"
             "2. If the context doesn't fully answer the question, acknowledge this\n"
             "3. Use simple language and provide examples when helpful\n"
             "4. Structure your response logically with key points\n"
             "5. Include references to the source materials when relevant\n"
             "6. If you're making inferences beyond the provided context, clearly state this"),
            ("user", 
             "Context from lecture materials:\n{context}\n\n"
             "Student question: {question}\n\n"
             "Please provide a clear and educational explanation.")
        ])
    
    def explain(self, question: str, context: str, metadata: Dict = None) -> Dict:
        """
        Generate an explanation based on retrieved context
        
        Args:
            question: User's question
            context: Retrieved context from documents
            metadata: Optional metadata about the retrieval
            
        Returns:
            Dictionary with explanation and metadata
        """
        # Generate explanation
        chain = self.explanation_prompt | self.llm
        response = chain.invoke({
            "question": question,
            "context": context
        })
        
        explanation = response.content.strip()
        
        return {
            'question': question,
            'explanation': explanation,
            'context_used': context,
            'metadata': metadata or {}
        }
    
    def explain_with_follow_up(self, question: str, context: str) -> Dict:
        """
        Generate explanation with suggested follow-up questions
        
        Args:
            question: User's question
            context: Retrieved context from documents
            
        Returns:
            Dictionary with explanation and follow-up questions
        """
        # Extended prompt for follow-up questions
        follow_up_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an expert educational assistant. Provide a clear explanation and then suggest "
             "3 relevant follow-up questions that would deepen understanding of the topic."),
            ("user",
             "Context from lecture materials:\n{context}\n\n"
             "Student question: {question}\n\n"
             "Please provide:\n1. A clear explanation\n2. Three follow-up questions\n\n"
             "Format your response as:\n"
             "EXPLANATION:\n[your explanation]\n\n"
             "FOLLOW-UP QUESTIONS:\n1. [question 1]\n2. [question 2]\n3. [question 3]")
        ])
        
        chain = follow_up_prompt | self.llm
        response = chain.invoke({
            "question": question,
            "context": context
        })
        
        content = response.content.strip()
        
        # Parse response
        parts = content.split("FOLLOW-UP QUESTIONS:")
        explanation = parts[0].replace("EXPLANATION:", "").strip()
        follow_ups = parts[1].strip() if len(parts) > 1 else ""
        
        return {
            'question': question,
            'explanation': explanation,
            'follow_up_questions': follow_ups,
            'context_used': context
        }
