"""
Research Agent - Orchestrates complex research workflows
"""
from typing import List, Dict, Optional
from agents.rag_agent import RAGAgent
from agents.task_delegator import TaskDelegator
from tools.web_search import WebSearchTool, WebScraperTool
from tools.summarizer import SummarizerTool
from utils.llm_client import LLMClient


class ResearchAgent:
    """
    Advanced research agent that orchestrates complex research workflows
    combining RAG, web search, and intelligent task delegation
    """
    
    def __init__(self, collection_name: Optional[str] = None):
        """Initialize research agent with all necessary tools"""
        self.rag_agent = RAGAgent(collection_name=collection_name)
        self.task_delegator = TaskDelegator()
        self.web_search = WebSearchTool()
        self.web_scraper = WebScraperTool()
        self.summarizer = SummarizerTool()
        self.llm = LLMClient()
        
        print("✓ Research Agent initialized with all tools")
    
    def deep_research(
        self, 
        query: str, 
        use_web: bool = True,
        use_kb: bool = True,
        max_iterations: int = 5
    ) -> Dict:
        """
        Perform deep research on a complex query
        
        Args:
            query: Research query
            use_web: Whether to use web search
            use_kb: Whether to use knowledge base
            max_iterations: Maximum research iterations
            
        Returns:
            Comprehensive research results
        """
        print(f"\n{'='*60}")
        print(f"Starting Deep Research: {query}")
        print(f"{'='*60}\n")
        
        # Step 1: Decompose the task
        print("📋 Step 1: Decomposing task into subtasks...")
        research_plan = self.task_delegator.create_research_plan(query)
        subtasks = research_plan['subtasks']
        
        print(f"   Created {len(subtasks)} subtasks")
        for task in subtasks[:3]:  # Show first 3
            print(f"   - {task['title']}")
        
        # Step 2: Gather information from multiple sources
        print("\n🔍 Step 2: Gathering information from sources...")
        
        gathered_info = []
        
        # From knowledge base
        if use_kb:
            print("   Searching knowledge base...")
            kb_results = self.rag_agent.research(query, depth='comprehensive')
            if kb_results['num_sources'] > 0:
                gathered_info.append({
                    'source': 'knowledge_base',
                    'content': kb_results['summary'],
                    'metadata': {'num_sources': kb_results['num_sources']}
                })
                print(f"   ✓ Found {kb_results['num_sources']} relevant documents")
        
        # From web search
        if use_web:
            print("   Searching web...")
            try:
                search_results = self.web_search.get_search_results(query, num_results=5)
                if search_results:
                    # Get snippets from search results
                    web_content = "\n\n".join([
                        f"{r['title']}: {r['snippet']}" 
                        for r in search_results[:3]
                    ])
                    gathered_info.append({
                        'source': 'web_search',
                        'content': web_content,
                        'metadata': {'num_results': len(search_results)}
                    })
                    print(f"   ✓ Retrieved {len(search_results)} web results")
            except Exception as e:
                print(f"   ⚠ Web search error: {e}")
        
        # Step 3: Process each subtask
        print("\n⚙️  Step 3: Processing subtasks...")
        
        subtask_results = []
        for i, subtask in enumerate(subtasks[:max_iterations], 1):
            print(f"   Processing subtask {i}/{min(len(subtasks), max_iterations)}: {subtask['title'][:50]}...")
            
            # Create context from gathered info
            context = "\n\n".join([info['content'] for info in gathered_info])
            
            # Generate answer for subtask
            result = self.llm.analyze_with_context(
                subtask['title'],
                context,
                instruction="Provide a detailed analysis based on the available context."
            )
            
            subtask_results.append({
                'subtask': subtask['title'],
                'result': result
            })
        
        # Step 4: Synthesize findings
        print("\n🔄 Step 4: Synthesizing findings...")
        
        all_content = [info['content'] for info in gathered_info]
        all_content.extend([r['result'] for r in subtask_results])
        
        synthesis = self.summarizer.synthesize_multiple_sources(all_content[:5])
        
        # Step 5: Generate final report
        print("\n📊 Step 5: Generating final report...")
        
        final_report = self._generate_final_report(
            query, 
            research_plan, 
            gathered_info, 
            subtask_results, 
            synthesis
        )
        
        print(f"\n{'='*60}")
        print("✓ Research Complete!")
        print(f"{'='*60}\n")
        
        return {
            'query': query,
            'research_plan': research_plan,
            'sources_used': len(gathered_info),
            'subtasks_completed': len(subtask_results),
            'synthesis': synthesis,
            'final_report': final_report,
            'raw_data': {
                'gathered_info': gathered_info,
                'subtask_results': subtask_results
            }
        }
    
    def _generate_final_report(
        self, 
        query: str, 
        plan: Dict,
        gathered_info: List[Dict],
        subtask_results: List[Dict],
        synthesis: str
    ) -> str:
        """Generate a comprehensive final report"""
        
        report = f"""
# Research Report: {query}

## Executive Summary
{synthesis}

## Research Approach
{plan['plan'][:500]}...

## Key Findings

"""
        
        # Add subtask results
        for i, result in enumerate(subtask_results, 1):
            report += f"\n### Finding {i}: {result['subtask']}\n"
            report += f"{result['result'][:400]}...\n"
        
        # Add sources
        report += "\n## Sources\n"
        for i, info in enumerate(gathered_info, 1):
            source_type = info['source'].replace('_', ' ').title()
            report += f"{i}. {source_type} ({info['metadata']})\n"
        
        report += "\n## Conclusion\n"
        report += "Based on the comprehensive analysis above, "
        report += synthesis[-300:] if len(synthesis) > 300 else synthesis
        
        return report
    
    def compare_topics(self, topic1: str, topic2: str) -> Dict:
        """
        Compare two topics
        
        Args:
            topic1: First topic
            topic2: Second topic
            
        Returns:
            Comparison results
        """
        print(f"\n🔍 Comparing: {topic1} vs {topic2}")
        
        # Research both topics
        research1 = self.rag_agent.research(topic1, depth='standard')
        research2 = self.rag_agent.research(topic2, depth='standard')
        
        # Compare
        comparison = self.summarizer.compare_documents(
            research1['summary'],
            research2['summary']
        )
        
        return {
            'topic1': topic1,
            'topic2': topic2,
            'research1': research1,
            'research2': research2,
            'comparison': comparison
        }
    
    def quick_answer(self, question: str) -> str:
        """
        Get a quick answer combining KB and web search
        
        Args:
            question: Question to answer
            
        Returns:
            Answer
        """
        # Try KB first
        kb_context = self.rag_agent.vector_store.get_context_for_query(question, n_results=3)
        
        # Try web search
        try:
            web_results = self.web_search.get_search_results(question, num_results=3)
            web_context = "\n".join([f"{r['title']}: {r['snippet']}" for r in web_results[:2]])
        except:
            web_context = ""
        
        # Combine contexts
        combined_context = f"Knowledge Base:\n{kb_context}\n\nWeb Results:\n{web_context}"
        
        return self.llm.analyze_with_context(question, combined_context)
    
    def add_knowledge(self, content: str, source: str = "manual"):
        """
        Add knowledge to the system
        
        Args:
            content: Content to add
            source: Source identifier
        """
        self.rag_agent.add_documents([content], [{"source": source}])
        print(f"✓ Added knowledge from {source}")
    
    def research_from_urls(self, urls: List[str], query: str) -> Dict:
        """
        Research specific URLs
        
        Args:
            urls: List of URLs to research
            query: Research query
            
        Returns:
            Research results
        """
        print(f"\n📄 Researching {len(urls)} URLs...")
        
        # Scrape URLs
        scraped_content = self.web_scraper.scrape_multiple_urls(urls)
        
        # Add to knowledge base temporarily
        for url, content in scraped_content.items():
            if content:
                self.add_knowledge(content[:5000], source=url)  # Limit content size
        
        # Perform research
        return self.deep_research(query, use_web=False, use_kb=True)


if __name__ == "__main__":
    # Test research agent
    agent = ResearchAgent(collection_name="test_research")
    
    # Add some test knowledge
    agent.add_knowledge(
        "AI agents are autonomous systems that can perceive their environment and take actions to achieve goals.",
        source="test"
    )
    
    # Quick answer
    print("Testing quick answer...")
    answer = agent.quick_answer("What are AI agents?")
    print(f"\nAnswer: {answer[:200]}...")
    
    # Deep research (commented out for quick test)
    # result = agent.deep_research("Explain the architecture of RAG systems")
    # print(f"\n\nFinal Report:\n{result['final_report']}")
