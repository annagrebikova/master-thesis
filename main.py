"""
Command-line interface for the Educational Assistant
"""

import sys
import argparse
from src.educational_assistant import EducationalAssistant


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Multi-Agent Educational Assistant - RAG-based Q&A system"
    )
    
    parser.add_argument(
        'command',
        choices=['ingest', 'ask', 'interactive'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--path',
        help='Path to document(s) to ingest'
    )
    
    parser.add_argument(
        '--question',
        help='Question to ask'
    )
    
    parser.add_argument(
        '--k',
        type=int,
        default=4,
        help='Number of relevant documents to retrieve (default: 4)'
    )
    
    parser.add_argument(
        '--follow-up',
        action='store_true',
        help='Include follow-up questions in response'
    )
    
    parser.add_argument(
        '--save',
        help='Path to save vector store'
    )
    
    parser.add_argument(
        '--load',
        help='Path to load vector store from'
    )
    
    args = parser.parse_args()
    
    # Initialize assistant
    assistant = EducationalAssistant()
    
    # Handle commands
    if args.command == 'ingest':
        if not args.path:
            print("Error: --path required for ingest command")
            sys.exit(1)
        
        print(f"\n{'='*60}")
        print("INGESTING DOCUMENTS")
        print(f"{'='*60}")
        
        result = assistant.ingest_documents(args.path)
        print(f"\n✓ Successfully ingested {result['num_documents']} document(s)")
        print(f"✓ Created {result['num_chunks']} chunks")
        
        if args.save:
            assistant.save_vector_store(args.save)
            print(f"✓ Vector store saved to {args.save}")
    
    elif args.command == 'ask':
        if not args.question:
            print("Error: --question required for ask command")
            sys.exit(1)
        
        # Load vector store if specified
        if args.load:
            print(f"Loading vector store from {args.load}...")
            assistant.load_vector_store(args.load)
        elif not args.path:
            print("Error: Either --path or --load required")
            sys.exit(1)
        else:
            assistant.ingest_documents(args.path)
        
        print(f"\n{'='*60}")
        print("QUESTION")
        print(f"{'='*60}")
        print(args.question)
        
        result = assistant.ask(args.question, k=args.k, include_follow_up=args.follow_up)
        
        print(f"\n{'='*60}")
        print("ANSWER")
        print(f"{'='*60}")
        print(result['answer'])
        
        print(f"\n{'='*60}")
        print("SOURCES")
        print(f"{'='*60}")
        for i, source in enumerate(set(result['sources']), 1):
            print(f"{i}. {source}")
        
        if args.follow_up and 'follow_up_questions' in result:
            print(f"\n{'='*60}")
            print("FOLLOW-UP QUESTIONS")
            print(f"{'='*60}")
            print(result['follow_up_questions'])
    
    elif args.command == 'interactive':
        # Load or ingest documents
        if args.load:
            print(f"Loading vector store from {args.load}...")
            assistant.load_vector_store(args.load)
        elif args.path:
            print(f"Ingesting documents from {args.path}...")
            assistant.ingest_documents(args.path)
        else:
            print("Error: Either --path or --load required for interactive mode")
            sys.exit(1)
        
        print(f"\n{'='*60}")
        print("INTERACTIVE MODE")
        print(f"{'='*60}")
        print("Ask questions about your lecture materials!")
        print("Commands: 'quit' or 'exit' to stop, 'feedback' to provide feedback")
        print(f"{'='*60}\n")
        
        last_question = None
        last_answer = None
        
        while True:
            try:
                user_input = input("\n💬 Your question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'feedback':
                    if not last_question or not last_answer:
                        print("❌ No previous answer to provide feedback on")
                        continue
                    
                    feedback_text = input("📝 Your feedback: ").strip()
                    rating_input = input("⭐ Rating (1-5, or press Enter to skip): ").strip()
                    rating = int(rating_input) if rating_input.isdigit() else None
                    
                    assistant.provide_feedback(last_question, last_answer, feedback_text, rating)
                    print("✓ Feedback recorded. Thank you!")
                    
                    improve = input("Would you like an improved answer? (y/n): ").strip().lower()
                    if improve == 'y':
                        result = assistant.improve_based_on_feedback(
                            last_question, last_answer, feedback_text
                        )
                        print(f"\n{'='*60}")
                        print("IMPROVED ANSWER")
                        print(f"{'='*60}")
                        print(result['improved_response'])
                        last_answer = result['improved_response']
                    continue
                
                if not user_input:
                    continue
                
                # Ask question
                result = assistant.ask(user_input, k=args.k)
                
                print(f"\n{'='*60}")
                print("ANSWER")
                print(f"{'='*60}")
                print(result['answer'])
                
                print(f"\n📚 Sources: {', '.join(set(result['sources']))}")
                
                last_question = user_input
                last_answer = result['answer']
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
