"""
Demo Script - Showcases RAG Agent Capabilities
"""
from agents.research_agent import ResearchAgent
from workflows.research_workflow import create_comparative_research_workflow
from colorama import init, Fore, Style

init(autoreset=True)


def print_section(title: str):
    """Print a section header"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{title}")
    print(f"{'='*70}{Style.RESET_ALL}\n")


def demo_basic_rag():
    """Demonstrate basic RAG functionality"""
    print_section("Demo 1: Basic RAG Agent")
    
    agent = ResearchAgent(collection_name="demo_basic")
    
    # Add some knowledge
    print("📚 Adding knowledge to the system...")
    
    knowledge_base = [
        """RAG (Retrieval-Augmented Generation) is an AI framework that combines 
        information retrieval with text generation. It retrieves relevant documents 
        from a knowledge base and uses them to generate more accurate and contextual responses.""",
        
        """Vector databases store data as mathematical embeddings, enabling semantic 
        similarity search. Popular vector databases include ChromaDB, Pinecone, and Weaviate.""",
        
        """AI agents are autonomous systems that can perceive their environment, make decisions, 
        and take actions to achieve specific goals. They can be reactive, deliberative, or hybrid.""",
        
        """Task delegation in AI systems involves breaking down complex tasks into smaller 
        subtasks that can be handled by specialized components or agents.""",
    ]
    
    for i, knowledge in enumerate(knowledge_base, 1):
        agent.add_knowledge(knowledge, source=f"demo_doc_{i}")
    
    print(f"{Fore.GREEN}✓ Added {len(knowledge_base)} documents\n{Style.RESET_ALL}")
    
    # Query the system
    print("🔍 Querying the RAG system...")
    question = "What is RAG and how does it work?"
    
    answer = agent.quick_answer(question)
    
    print(f"{Fore.YELLOW}Question: {question}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Answer: {answer}{Style.RESET_ALL}\n")


def demo_task_delegation():
    """Demonstrate task delegation"""
    print_section("Demo 2: Task Delegation")
    
    agent = ResearchAgent(collection_name="demo_tasks")
    
    complex_query = """Analyze the impact of artificial intelligence on healthcare, 
    including current applications, challenges, ethical considerations, and future prospects."""
    
    print(f"{Fore.YELLOW}Complex Query:{Style.RESET_ALL} {complex_query}\n")
    print("🧠 Breaking down into subtasks...\n")
    
    plan = agent.task_delegator.create_research_plan(complex_query)
    
    print(f"{Fore.GREEN}Research Plan:{Style.RESET_ALL}")
    print(plan['plan'][:500] + "...\n")
    
    print(f"{Fore.GREEN}Identified {len(plan['subtasks'])} subtasks:{Style.RESET_ALL}")
    for i, task in enumerate(plan['subtasks'][:5], 1):
        print(f"  {i}. {task['title']}")
    print()


def demo_web_search():
    """Demonstrate web search integration"""
    print_section("Demo 3: Web Search Integration")
    
    from tools.web_search import WebSearchTool
    
    search_tool = WebSearchTool()
    
    query = "Latest developments in AI agents 2024"
    
    print(f"{Fore.YELLOW}Search Query:{Style.RESET_ALL} {query}\n")
    print("🌐 Searching the web...\n")
    
    results = search_tool.get_search_results(query, num_results=3)
    
    print(f"{Fore.GREEN}Top 3 Results:{Style.RESET_ALL}\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   {Fore.CYAN}{result['link']}{Style.RESET_ALL}")
        print(f"   {result['snippet']}\n")


def demo_document_processing():
    """Demonstrate document processing"""
    print_section("Demo 4: Document Processing")
    
    from tools.document_loader import DocumentLoader
    
    loader = DocumentLoader()
    
    # Create sample text
    sample_text = """
    Artificial Intelligence has revolutionized numerous industries in recent years.
    Machine learning algorithms can now process vast amounts of data and identify 
    patterns that humans might miss. Deep learning, a subset of machine learning,
    uses neural networks with multiple layers to achieve impressive results in 
    image recognition, natural language processing, and game playing.
    
    The applications of AI are diverse, ranging from healthcare diagnosis to 
    autonomous vehicles, from financial forecasting to personalized recommendations.
    However, these advances also raise important ethical questions about privacy,
    bias, and the future of work.
    """ * 5  # Repeat to have enough text
    
    print("📄 Processing sample document...\n")
    
    chunks = loader.chunk_text(sample_text, chunk_size=200, chunk_overlap=50)
    
    print(f"{Fore.GREEN}✓ Created {len(chunks)} chunks{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}First chunk:{Style.RESET_ALL}")
    print(f"{chunks[0][:150]}...\n")


def demo_workflow():
    """Demonstrate workflow orchestration"""
    print_section("Demo 5: Workflow Orchestration")
    
    agent = ResearchAgent(collection_name="demo_workflow")
    
    # Add some initial knowledge
    agent.add_knowledge(
        "Machine Learning is a subset of AI that enables systems to learn from data.",
        source="ml_basics"
    )
    agent.add_knowledge(
        "Deep Learning uses neural networks with multiple layers for complex pattern recognition.",
        source="dl_basics"
    )
    
    print("🔄 Creating comparative research workflow...\n")
    
    workflow = create_comparative_research_workflow(
        agent, 
        "Machine Learning", 
        "Deep Learning"
    )
    
    print(f"{Fore.GREEN}Workflow: {workflow.workflow_name}{Style.RESET_ALL}")
    print(f"Steps: {len(workflow.steps)}\n")
    
    # Execute workflow
    print("▶️  Executing workflow...\n")
    result = workflow.execute()
    
    print(f"\n{Fore.GREEN}Workflow Status: {result['status']}{Style.RESET_ALL}")
    
    if 'synthesize' in result['results']:
        print(f"\n{Fore.YELLOW}Synthesis:{Style.RESET_ALL}")
        print(result['results']['synthesize'][:300] + "...\n")


def demo_deep_research():
    """Demonstrate deep research capability"""
    print_section("Demo 6: Deep Research")
    
    agent = ResearchAgent(collection_name="demo_deep")
    
    # Add comprehensive knowledge base
    knowledge_items = [
        "Neural networks are computing systems inspired by biological neural networks.",
        "Transformers revolutionized NLP with their attention mechanism.",
        "GPT models use autoregressive generation for text completion.",
        "BERT uses bidirectional training for better context understanding.",
        "Vision transformers apply transformer architecture to image processing.",
    ]
    
    for item in knowledge_items:
        agent.add_knowledge(item, source="ai_knowledge")
    
    query = "Explain the evolution of neural network architectures"
    
    print(f"{Fore.YELLOW}Research Query:{Style.RESET_ALL} {query}\n")
    print("🔬 Performing deep research (this may take a moment)...\n")
    
    # Note: We'll use use_web=False for demo to avoid API calls
    result = agent.deep_research(query, use_web=False, use_kb=True, max_iterations=3)
    
    print(f"\n{Fore.GREEN}Research Complete!{Style.RESET_ALL}")
    print(f"Sources used: {result['sources_used']}")
    print(f"Subtasks completed: {result['subtasks_completed']}\n")
    print(f"{Fore.YELLOW}Executive Summary:{Style.RESET_ALL}")
    print(result['synthesis'][:400] + "...\n")


def main():
    """Run all demos"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"RAG Agent Demo Suite")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("This demo showcases the capabilities of the RAG agent system.\n")
    
    demos = [
        ("Basic RAG", demo_basic_rag),
        ("Task Delegation", demo_task_delegation),
        ("Web Search", demo_web_search),
        ("Document Processing", demo_document_processing),
        ("Workflow Orchestration", demo_workflow),
        ("Deep Research", demo_deep_research),
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        print(f"{Fore.GREEN}[{i}/{len(demos)}] Running: {name}{Style.RESET_ALL}")
        
        try:
            demo_func()
        except Exception as e:
            print(f"{Fore.RED}Error in demo: {e}{Style.RESET_ALL}\n")
        
        if i < len(demos):
            input(f"\n{Fore.CYAN}Press Enter to continue to next demo...{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}{'='*70}")
    print(f"All Demos Complete!")
    print(f"{'='*70}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
