"""
Test Script - Verify RAG Agent Installation
"""
import sys
from colorama import init, Fore, Style

init(autoreset=True)


def print_status(test_name, passed, message=""):
    """Print test status"""
    if passed:
        print(f"✓ {Fore.GREEN}{test_name}{Style.RESET_ALL}")
    else:
        print(f"✗ {Fore.RED}{test_name}{Style.RESET_ALL}")
        if message:
            print(f"  Error: {message}")


def test_imports():
    """Test if all required modules can be imported"""
    print(f"\n{Fore.CYAN}Testing Imports...{Style.RESET_ALL}\n")
    
    tests = []
    
    # Core Python packages
    try:
        import os
        tests.append(("Python os module", True, ""))
    except Exception as e:
        tests.append(("Python os module", False, str(e)))
    
    # Third-party packages
    packages = [
        ("groq", "Groq API client"),
        ("dotenv", "python-dotenv"),
        ("chromadb", "ChromaDB"),
        ("sentence_transformers", "Sentence Transformers"),
        ("requests", "Requests"),
        ("bs4", "BeautifulSoup4"),
        ("pypdf", "PyPDF"),
        ("docx", "python-docx"),
        ("colorama", "Colorama"),
    ]
    
    for module_name, display_name in packages:
        try:
            __import__(module_name)
            tests.append((display_name, True, ""))
        except Exception as e:
            tests.append((display_name, False, str(e)))
    
    # Project modules
    try:
        from utils.llm_client import LLMClient
        tests.append(("utils.llm_client", True, ""))
    except Exception as e:
        tests.append(("utils.llm_client", False, str(e)))
    
    try:
        from utils.vector_store import VectorStore
        tests.append(("utils.vector_store", True, ""))
    except Exception as e:
        tests.append(("utils.vector_store", False, str(e)))
    
    try:
        from tools.web_search import WebSearchTool
        tests.append(("tools.web_search", True, ""))
    except Exception as e:
        tests.append(("tools.web_search", False, str(e)))
    
    try:
        from agents.rag_agent import RAGAgent
        tests.append(("agents.rag_agent", True, ""))
    except Exception as e:
        tests.append(("agents.rag_agent", False, str(e)))
    
    try:
        from agents.research_agent import ResearchAgent
        tests.append(("agents.research_agent", True, ""))
    except Exception as e:
        tests.append(("agents.research_agent", False, str(e)))
    
    # Print results
    for test_name, passed, message in tests:
        print_status(test_name, passed, message)
    
    passed_count = sum(1 for _, passed, _ in tests if passed)
    total_count = len(tests)
    
    print(f"\n{passed_count}/{total_count} imports successful")
    
    return passed_count == total_count


def test_environment():
    """Test environment configuration"""
    print(f"\n{Fore.CYAN}Testing Environment Configuration...{Style.RESET_ALL}\n")
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    tests = []
    
    # Check API keys
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and len(groq_key) > 20:
        tests.append(("GROQ_API_KEY", True, ""))
    else:
        tests.append(("GROQ_API_KEY", False, "Not found or invalid"))
    
    serper_key = os.getenv("SERPER_API_KEY")
    if serper_key and len(serper_key) > 20:
        tests.append(("SERPER_API_KEY", True, ""))
    else:
        tests.append(("SERPER_API_KEY", False, "Not found or invalid"))
    
    # Check configuration
    model = os.getenv("GROQ_MODEL")
    tests.append(("GROQ_MODEL configured", bool(model), model or "Not set"))
    
    # Print results
    for test_name, passed, message in tests:
        print_status(test_name, passed, message)
    
    passed_count = sum(1 for _, passed, _ in tests if passed)
    total_count = len(tests)
    
    print(f"\n{passed_count}/{total_count} environment checks passed")
    
    return passed_count == total_count


def test_llm_client():
    """Test LLM client"""
    print(f"\n{Fore.CYAN}Testing LLM Client...{Style.RESET_ALL}\n")
    
    try:
        from utils.llm_client import LLMClient
        
        client = LLMClient()
        print_status("LLM Client initialized", True)
        
        # Test simple generation
        response = client.generate("Say 'test successful' in one sentence.", temperature=0.3)
        
        if response and len(response) > 5:
            print_status("LLM generation works", True)
            print(f"  Response: {response[:100]}...")
            return True
        else:
            print_status("LLM generation works", False, "Empty or invalid response")
            return False
            
    except Exception as e:
        print_status("LLM Client test", False, str(e))
        return False


def test_vector_store():
    """Test vector store"""
    print(f"\n{Fore.CYAN}Testing Vector Store...{Style.RESET_ALL}\n")
    
    try:
        from utils.vector_store import VectorStore
        
        # Create test collection
        vs = VectorStore(collection_name="test_collection_temp")
        print_status("Vector Store initialized", True)
        
        # Add test documents
        docs = [
            "This is a test document about AI.",
            "Vector databases are useful for semantic search.",
        ]
        
        ids = vs.add_documents(docs, [{"source": "test"} for _ in docs])
        
        if len(ids) == len(docs):
            print_status("Documents added", True)
        else:
            print_status("Documents added", False, "ID count mismatch")
            return False
        
        # Search
        results = vs.search("AI and databases", n_results=2)
        
        if results['documents'] and len(results['documents']) > 0:
            print_status("Vector search works", True)
            print(f"  Found {len(results['documents'])} results")
            
            # Cleanup
            vs.delete_collection()
            return True
        else:
            print_status("Vector search works", False, "No results")
            return False
            
    except Exception as e:
        print_status("Vector Store test", False, str(e))
        return False


def test_web_search():
    """Test web search (optional - requires API call)"""
    print(f"\n{Fore.CYAN}Testing Web Search (optional)...{Style.RESET_ALL}\n")
    
    try:
        from tools.web_search import WebSearchTool
        
        search_tool = WebSearchTool()
        print_status("Web Search Tool initialized", True)
        
        # Note: This makes an actual API call
        results = search_tool.get_search_results("Python programming", num_results=2)
        
        if results and len(results) > 0:
            print_status("Web search works", True)
            print(f"  Found {len(results)} results")
            return True
        else:
            print_status("Web search works", False, "No results")
            return False
            
    except Exception as e:
        print_status("Web Search test", False, str(e))
        print("  Note: This is optional and requires valid Serper API key")
        return False


def test_rag_agent():
    """Test RAG agent"""
    print(f"\n{Fore.CYAN}Testing RAG Agent...{Style.RESET_ALL}\n")
    
    try:
        from agents.rag_agent import RAGAgent
        
        agent = RAGAgent(collection_name="test_rag_temp")
        print_status("RAG Agent initialized", True)
        
        # Add test knowledge
        docs = [
            "RAG stands for Retrieval-Augmented Generation.",
            "It combines retrieval with text generation for better accuracy.",
        ]
        
        agent.add_documents(docs, [{"source": "test"} for _ in docs])
        print_status("Documents added to RAG", True)
        
        # Query
        answer = agent.query("What is RAG?", n_results=2)
        
        if answer and len(answer) > 10:
            print_status("RAG query works", True)
            print(f"  Answer: {answer[:100]}...")
            
            # Cleanup
            agent.vector_store.delete_collection()
            return True
        else:
            print_status("RAG query works", False, "Empty answer")
            return False
            
    except Exception as e:
        print_status("RAG Agent test", False, str(e))
        return False


def test_research_agent():
    """Test research agent"""
    print(f"\n{Fore.CYAN}Testing Research Agent...{Style.RESET_ALL}\n")
    
    try:
        from agents.research_agent import ResearchAgent
        
        agent = ResearchAgent(collection_name="test_research_temp")
        print_status("Research Agent initialized", True)
        
        # Add test knowledge
        agent.add_knowledge(
            "Artificial intelligence enables machines to perform tasks requiring human intelligence.",
            source="test"
        )
        print_status("Knowledge added", True)
        
        # Quick answer test
        answer = agent.quick_answer("What is AI?")
        
        if answer and len(answer) > 10:
            print_status("Quick answer works", True)
            print(f"  Answer: {answer[:100]}...")
            
            # Cleanup
            agent.rag_agent.vector_store.delete_collection()
            return True
        else:
            print_status("Quick answer works", False, "Empty answer")
            return False
            
    except Exception as e:
        print_status("Research Agent test", False, str(e))
        return False


def main():
    """Run all tests"""
    print(f"{Fore.CYAN}{'='*70}")
    print(f"RAG Agent System Test")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    tests = [
        ("Imports", test_imports),
        ("Environment", test_environment),
        ("LLM Client", test_llm_client),
        ("Vector Store", test_vector_store),
        ("RAG Agent", test_rag_agent),
        ("Research Agent", test_research_agent),
        ("Web Search", test_web_search),  # Optional, makes API call
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n{Fore.RED}Unexpected error in {test_name}: {e}{Style.RESET_ALL}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"Test Summary")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if result else f"{Fore.RED}FAIL{Style.RESET_ALL}"
        print(f"  {test_name}: {status}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print(f"\n{Fore.GREEN}🎉 All tests passed! Your RAG agent is ready to use.{Style.RESET_ALL}")
        print(f"\nRun: {Fore.CYAN}python main.py{Style.RESET_ALL} to start")
        return 0
    else:
        print(f"\n{Fore.YELLOW}⚠ Some tests failed. Please check the errors above.{Style.RESET_ALL}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
