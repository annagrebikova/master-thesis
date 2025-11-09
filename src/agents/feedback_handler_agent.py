"""
Feedback Handler Agent
Responsible for processing user feedback and improving system responses
"""

from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime


class FeedbackHandlerAgent:
    """Agent responsible for handling user feedback and improving responses"""
    
    def __init__(self, llm_model: str = "gpt-3.5-turbo"):
        """
        Initialize feedback handler agent
        
        Args:
            llm_model: OpenAI model to use
        """
        self.llm = ChatOpenAI(model=llm_model, temperature=0.3)
        self.feedback_history = []
        
        # Prompt for analyzing feedback
        self.feedback_analysis_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a feedback analysis assistant. Analyze user feedback to identify:\n"
             "1. What the user found helpful or unhelpful\n"
             "2. What information might be missing\n"
             "3. How to improve future responses\n"
             "Be specific and actionable in your analysis."),
            ("user",
             "Original question: {question}\n\n"
             "System response: {response}\n\n"
             "User feedback: {feedback}\n\n"
             "Please analyze this feedback and provide insights.")
        ])
        
        # Prompt for generating improved response
        self.improvement_prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an educational assistant improving a previous response based on user feedback. "
             "Address the user's concerns while maintaining accuracy and clarity."),
            ("user",
             "Original question: {question}\n\n"
             "Previous response: {previous_response}\n\n"
             "User feedback: {feedback}\n\n"
             "Context: {context}\n\n"
             "Please provide an improved response that addresses the feedback.")
        ])
    
    def record_feedback(self, question: str, response: str, feedback: str, 
                       rating: int = None) -> Dict:
        """
        Record user feedback
        
        Args:
            question: Original question
            response: System response
            feedback: User's feedback text
            rating: Optional numerical rating (1-5)
            
        Returns:
            Dictionary with recorded feedback
        """
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'response': response,
            'feedback': feedback,
            'rating': rating
        }
        
        self.feedback_history.append(feedback_entry)
        
        return {
            'status': 'recorded',
            'feedback_id': len(self.feedback_history) - 1,
            'entry': feedback_entry
        }
    
    def analyze_feedback(self, question: str, response: str, feedback: str) -> Dict:
        """
        Analyze user feedback to extract insights
        
        Args:
            question: Original question
            response: System response
            feedback: User's feedback
            
        Returns:
            Dictionary with analysis results
        """
        chain = self.feedback_analysis_prompt | self.llm
        analysis_response = chain.invoke({
            "question": question,
            "response": response,
            "feedback": feedback
        })
        
        return {
            'question': question,
            'feedback': feedback,
            'analysis': analysis_response.content.strip()
        }
    
    def improve_response(self, question: str, previous_response: str, 
                        feedback: str, context: str) -> Dict:
        """
        Generate an improved response based on feedback
        
        Args:
            question: Original question
            previous_response: Previous system response
            feedback: User's feedback
            context: Retrieved context
            
        Returns:
            Dictionary with improved response
        """
        chain = self.improvement_prompt | self.llm
        improved = chain.invoke({
            "question": question,
            "previous_response": previous_response,
            "feedback": feedback,
            "context": context
        })
        
        # Record the feedback
        self.record_feedback(question, previous_response, feedback)
        
        return {
            'question': question,
            'improved_response': improved.content.strip(),
            'original_response': previous_response,
            'feedback_applied': feedback
        }
    
    def get_feedback_summary(self) -> Dict:
        """
        Get summary of all feedback collected
        
        Returns:
            Dictionary with feedback statistics
        """
        if not self.feedback_history:
            return {
                'total_feedback': 0,
                'message': 'No feedback collected yet'
            }
        
        ratings = [f['rating'] for f in self.feedback_history if f['rating'] is not None]
        
        return {
            'total_feedback': len(self.feedback_history),
            'with_ratings': len(ratings),
            'average_rating': sum(ratings) / len(ratings) if ratings else None,
            'recent_feedback': self.feedback_history[-5:]  # Last 5 feedback entries
        }
