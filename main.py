"""
Main Application - RAG Agent for Deep Research
"""
import argparse
import sys
from colorama import init, Fore, Style
from agents.research_agent import ResearchAgent
from workflows.research_workflow import (
    create_document_analysis_workflow,
    create_comparative_research_workflow
)

# Initialize colorama for colored output
init(autoreset=True)


class RAGApplication:
    """Main application class for RAG agent"""
    
    def __init__(self):
        """Initialize the application"""
        print(f"{Fore.CYAN}{'='*70}")
        print(f"{Fore.CYAN}RAG Agent for Deep Research & Task Delegation")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        self.agent = ResearchAgent(collection_name="main_research")
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print(f"{Fore.GREEN}🤖 Interactive Mode Started{Style.RESET_ALL}")
        print("Type 'help' for commands, 'exit' to quit\n")
        
        conversation_history = []
        
        while True:
            try:
                user_input = input(f"{Fore.YELLOW}You: {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print(f"\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
                    break
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                if user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                
                if user_input.lower().startswith('deep '):
                    query = user_input[5:]
                    self.deep_research_mode(query)
                    continue
                
                if user_input.lower().startswith('compare '):
                    parts = user_input[8:].split(' vs ')
                    if len(parts) == 2:
                        self.compare_mode(parts[0].strip(), parts[1].strip())
                    else:
                        print(f"{Fore.RED}Usage: compare <topic1> vs <topic2>{Style.RESET_ALL}")
                    continue
                
                # Default: quick answer
                print(f"\n{Fore.CYAN}🤔 Thinking...{Style.RESET_ALL}\n")
                answer = self.agent.quick_answer(user_input)
                
                print(f"{Fore.GREEN}Agent: {Style.RESET_ALL}{answer}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}\n")
    
    def deep_research_mode(self, query: str):
        """Perform deep research"""
        result = self.agent.deep_research(query, use_web=True, use_kb=True)
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"RESEARCH REPORT")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        print(result['final_report'])
        print(f"\n{Fore.CYAN}Sources used: {result['sources_used']}")
        print(f"Subtasks completed: {result['subtasks_completed']}{Style.RESET_ALL}\n")
    
    def compare_mode(self, topic1: str, topic2: str):
        """Compare two topics"""
        print(f"\n{Fore.CYAN}🔍 Comparing: {topic1} vs {topic2}{Style.RESET_ALL}\n")
        
        result = self.agent.compare_topics(topic1, topic2)
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"COMPARISON REPORT")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        print(result['comparison'])
        print()
    
    def document_mode(self, file_path: str, action: str = 'analyze'):
        """Process a document"""
        print(f"\n{Fore.CYAN}📄 Processing document: {file_path}{Style.RESET_ALL}\n")
        
        if action == 'analyze':
            workflow = create_document_analysis_workflow(self.agent, file_path)
            result = workflow.execute()
            
            print(f"\n{Fore.GREEN}Analysis Results:{Style.RESET_ALL}")
            if 'summarize' in result['results']:
                print(f"\nSummary:\n{result['results']['summarize']}")
            if 'insights' in result['results']:
                print(f"\nInsights:\n{result['results']['insights']['analysis']}")
        
        elif action == 'add':
            num_chunks = self.agent.rag_agent.add_document_file(file_path)
            print(f"{Fore.GREEN}✓ Added {num_chunks} chunks to knowledge base{Style.RESET_ALL}")
    
    def research_mode(self, query: str):
        """Perform standard research"""
        print(f"\n{Fore.CYAN}🔍 Researching: {query}{Style.RESET_ALL}\n")
        
        result = self.agent.rag_agent.research(query, depth='comprehensive')
        
        print(f"\n{Fore.GREEN}Research Summary:{Style.RESET_ALL}\n")
        print(result['summary'])
        print(f"\n{Fore.CYAN}Based on {result['num_sources']} sources{Style.RESET_ALL}\n")
    
    def show_stats(self):
        """Show system statistics"""
        stats = self.agent.rag_agent.get_stats()
        
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"System Statistics")
        print(f"{'='*50}{Style.RESET_ALL}")
        print(f"Collection: {stats['name']}")
        print(f"Documents: {stats['document_count']}")
        print(f"Storage: {stats['persist_directory']}")
        print()
    
    def show_help(self):
        """Show help information"""
        help_text = f"""
{Fore.CYAN}{'='*70}
Available Commands
{'='*70}{Style.RESET_ALL}

{Fore.GREEN}Interactive Mode:{Style.RESET_ALL}
  <question>          Ask any question (quick answer)
  deep <query>        Perform deep research with task delegation
  compare <A> vs <B>  Compare two topics
  stats               Show system statistics
  help                Show this help message
  exit                Exit the application

{Fore.GREEN}Command Examples:{Style.RESET_ALL}
  What are AI agents?
  deep Explain the evolution of neural networks and their applications
  compare RAG vs Fine-tuning
  stats
  exit

{Fore.CYAN}{'='*70}{Style.RESET_ALL}
"""
        print(help_text)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='RAG Agent for Deep Research & Task Delegation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Interactive mode
  python main.py --mode research --query "What is quantum computing?"
  python main.py --mode deep --query "Compare AI architectures"
  python main.py --mode document --path "paper.pdf" --action analyze
  python main.py --mode compare --topics "RAG" "Fine-tuning"
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['interactive', 'research', 'deep', 'document', 'compare'],
        default='interactive',
        help='Operation mode'
    )
    
    parser.add_argument(
        '--query',
        type=str,
        help='Research query'
    )
    
    parser.add_argument(
        '--path',
        type=str,
        help='Document file path'
    )
    
    parser.add_argument(
        '--action',
        choices=['analyze', 'add'],
        default='analyze',
        help='Document action (analyze or add to KB)'
    )
    
    parser.add_argument(
        '--topics',
        nargs=2,
        metavar=('TOPIC1', 'TOPIC2'),
        help='Two topics to compare'
    )
    
    args = parser.parse_args()
    
    try:
        app = RAGApplication()
        
        if args.mode == 'interactive':
            app.interactive_mode()
        
        elif args.mode == 'research':
            if not args.query:
                print(f"{Fore.RED}Error: --query required for research mode{Style.RESET_ALL}")
                sys.exit(1)
            app.research_mode(args.query)
        
        elif args.mode == 'deep':
            if not args.query:
                print(f"{Fore.RED}Error: --query required for deep mode{Style.RESET_ALL}")
                sys.exit(1)
            app.deep_research_mode(args.query)
        
        elif args.mode == 'document':
            if not args.path:
                print(f"{Fore.RED}Error: --path required for document mode{Style.RESET_ALL}")
                sys.exit(1)
            app.document_mode(args.path, args.action)
        
        elif args.mode == 'compare':
            if not args.topics:
                print(f"{Fore.RED}Error: --topics required for compare mode{Style.RESET_ALL}")
                sys.exit(1)
            app.compare_mode(args.topics[0], args.topics[1])
    
    except Exception as e:
        print(f"{Fore.RED}Fatal Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
