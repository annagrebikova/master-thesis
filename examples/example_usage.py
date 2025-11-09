"""
Example script demonstrating the Educational Assistant
"""

import os
from src.educational_assistant import EducationalAssistant


def example_basic_usage():
    """Basic usage example"""
    print("="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    
    # Initialize assistant
    assistant = EducationalAssistant()
    
    # Ingest documents from a directory
    print("\n1. Ingesting documents...")
    result = assistant.ingest_documents("examples/lecture_materials")
    print(f"   ✓ Ingested {result['num_documents']} documents")
    print(f"   ✓ Created {result['num_chunks']} chunks")
    
    # Ask a question
    print("\n2. Asking a question...")
    question = "What is machine learning?"
    answer = assistant.ask(question)
    
    print(f"\n   Question: {answer['question']}")
    print(f"\n   Answer: {answer['answer']}")
    print(f"\n   Sources: {', '.join(set(answer['sources']))}")


def example_with_follow_up():
    """Example with follow-up questions"""
    print("\n" + "="*60)
    print("EXAMPLE 2: With Follow-up Questions")
    print("="*60)
    
    assistant = EducationalAssistant()
    assistant.ingest_documents("examples/lecture_materials")
    
    question = "Explain neural networks"
    result = assistant.ask(question, include_follow_up=True)
    
    print(f"\n   Question: {result['question']}")
    print(f"\n   Answer: {result['answer']}")
    
    if 'follow_up_questions' in result:
        print(f"\n   Follow-up Questions:\n   {result['follow_up_questions']}")


def example_feedback_handling():
    """Example with feedback handling"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Feedback Handling")
    print("="*60)
    
    assistant = EducationalAssistant()
    assistant.ingest_documents("examples/lecture_materials")
    
    # Ask initial question
    question = "What are the types of machine learning?"
    result = assistant.ask(question)
    
    print(f"\n   Initial Answer: {result['answer'][:200]}...")
    
    # Provide feedback
    print("\n   Providing feedback...")
    feedback = "Could you provide more specific examples of each type?"
    assistant.provide_feedback(question, result['answer'], feedback, rating=3)
    
    # Get improved response
    improved = assistant.improve_based_on_feedback(
        question, result['answer'], feedback
    )
    
    print(f"\n   Improved Answer: {improved['improved_response'][:200]}...")
    
    # Get feedback summary
    summary = assistant.get_feedback_summary()
    print(f"\n   Feedback Summary: {summary['total_feedback']} feedback entries collected")


def example_save_and_load():
    """Example saving and loading vector store"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Save and Load Vector Store")
    print("="*60)
    
    # Create and save
    print("\n   Creating vector store...")
    assistant1 = EducationalAssistant()
    assistant1.ingest_documents("examples/lecture_materials")
    assistant1.save_vector_store("vector_store")
    print("   ✓ Vector store saved")
    
    # Load in new instance
    print("\n   Loading vector store...")
    assistant2 = EducationalAssistant()
    assistant2.load_vector_store("vector_store")
    print("   ✓ Vector store loaded")
    
    # Use loaded store
    result = assistant2.ask("What is supervised learning?")
    print(f"\n   Question: {result['question']}")
    print(f"   Answer: {result['answer'][:200]}...")


if __name__ == "__main__":
    # Check if lecture materials exist
    if not os.path.exists("examples/lecture_materials"):
        print("Error: examples/lecture_materials directory not found")
        print("Please create some sample documents first")
        exit(1)
    
    # Check if there are any files
    files = os.listdir("examples/lecture_materials")
    supported_files = [f for f in files if f.endswith(('.pdf', '.docx', '.pptx'))]
    
    if not supported_files:
        print("Note: No lecture materials found in examples/lecture_materials/")
        print("Please add some PDF, DOCX, or PPTX files to test the system")
        exit(1)
    
    print("Running Educational Assistant Examples")
    print("="*60)
    
    try:
        example_basic_usage()
        example_with_follow_up()
        example_feedback_handling()
        example_save_and_load()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\nError running examples: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set OPENAI_API_KEY in .env file")
        print("2. Added lecture materials to examples/lecture_materials/")
        print("3. Installed all requirements: pip install -r requirements.txt")
