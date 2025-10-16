"""
Example: Building a Custom Research Workflow
"""
from agents.research_agent import ResearchAgent
from workflows.research_workflow import ResearchWorkflow
from tools.web_search import WebSearchTool


def create_competitive_analysis_workflow(agent: ResearchAgent, company: str) -> ResearchWorkflow:
    """
    Create a workflow for competitive analysis
    
    This example shows how to build a custom workflow for analyzing
    a company and its competitors
    """
    workflow = ResearchWorkflow(f"Competitive Analysis: {company}")
    
    # Step 1: Research the company
    def research_company(context):
        print(f"   Researching {company}...")
        # Try knowledge base first
        kb_result = agent.rag_agent.research(company, depth='standard')
        
        # Try web search
        try:
            web_tool = WebSearchTool()
            web_results = web_tool.get_search_results(f"{company} company overview", num_results=3)
            web_summary = "\n".join([r['snippet'] for r in web_results])
        except:
            web_summary = ""
        
        context['company_info'] = {
            'kb': kb_result['summary'],
            'web': web_summary
        }
        
        return f"Researched {company}"
    
    # Step 2: Identify competitors
    def identify_competitors(context):
        print(f"   Identifying competitors...")
        
        query = f"Who are the main competitors of {company}?"
        competitors = agent.llm.generate(query, temperature=0.3)
        
        context['competitors'] = competitors
        return competitors
    
    # Step 3: Research competitors
    def research_competitors(context):
        print(f"   Researching competitors...")
        
        competitors_text = context.get('competitors', '')
        # Extract competitor names (simple approach)
        # In production, you'd use more sophisticated extraction
        
        competitor_research = agent.llm.generate(
            f"Provide a brief analysis of each competitor mentioned: {competitors_text}",
            temperature=0.4
        )
        
        context['competitor_analysis'] = competitor_research
        return competitor_research
    
    # Step 4: SWOT Analysis
    def swot_analysis(context):
        print(f"   Performing SWOT analysis...")
        
        company_info = context['company_info']
        competitors = context.get('competitor_analysis', '')
        
        prompt = f"""Based on the following information, perform a SWOT analysis for {company}:

Company Information:
{company_info['kb'][:500]}

Competitor Analysis:
{competitors[:500]}

Provide:
- Strengths (3-5 points)
- Weaknesses (3-5 points)
- Opportunities (3-5 points)
- Threats (3-5 points)

SWOT Analysis:"""
        
        swot = agent.llm.generate(prompt, temperature=0.5)
        return swot
    
    # Step 5: Strategic Recommendations
    def recommendations(context):
        print(f"   Generating recommendations...")
        
        swot = context.get('result_swot', '')
        
        prompt = f"""Based on this SWOT analysis, provide 5 strategic recommendations for {company}:

{swot}

Recommendations:"""
        
        recs = agent.llm.generate(prompt, temperature=0.6)
        return recs
    
    # Add steps to workflow
    workflow.add_step('research', f'Research {company}', research_company)
    workflow.add_step('competitors', 'Identify Competitors', identify_competitors, 
                     dependencies=['research'])
    workflow.add_step('analyze_competitors', 'Analyze Competitors', research_competitors,
                     dependencies=['competitors'])
    workflow.add_step('swot', 'SWOT Analysis', swot_analysis,
                     dependencies=['research', 'analyze_competitors'])
    workflow.add_step('recommend', 'Strategic Recommendations', recommendations,
                     dependencies=['swot'])
    
    return workflow


def example_1_competitive_analysis():
    """Example 1: Competitive Analysis"""
    print("\n" + "="*70)
    print("Example 1: Competitive Analysis Workflow")
    print("="*70 + "\n")
    
    agent = ResearchAgent(collection_name="example_competitive")
    
    # Add some initial knowledge (in real use, you'd have more comprehensive data)
    agent.add_knowledge(
        "OpenAI is an AI research company known for GPT models and ChatGPT.",
        source="openai_info"
    )
    
    # Create and execute workflow
    company = "OpenAI"
    workflow = create_competitive_analysis_workflow(agent, company)
    
    result = workflow.execute()
    
    print("\n" + "="*70)
    print("Results")
    print("="*70 + "\n")
    
    if 'swot' in result['results']:
        print("SWOT Analysis:")
        print(result['results']['swot'])
        print()
    
    if 'recommend' in result['results']:
        print("\nStrategic Recommendations:")
        print(result['results']['recommend'])
        print()


def example_2_literature_review():
    """Example 2: Automated Literature Review"""
    print("\n" + "="*70)
    print("Example 2: Automated Literature Review")
    print("="*70 + "\n")
    
    agent = ResearchAgent(collection_name="example_literature")
    
    # Add academic papers (simulated)
    papers = [
        "Attention Is All You Need introduced the Transformer architecture in 2017.",
        "BERT uses bidirectional training for better language understanding.",
        "GPT-3 demonstrated few-shot learning capabilities with 175B parameters.",
        "Retrieval-Augmented Generation combines retrieval with generation for better factuality.",
    ]
    
    for i, paper in enumerate(papers, 1):
        agent.add_knowledge(paper, source=f"paper_{i}")
    
    # Perform literature review
    topic = "Evolution of transformer models in NLP"
    
    print(f"Topic: {topic}\n")
    print("Performing literature review...\n")
    
    result = agent.deep_research(topic, use_web=False, use_kb=True, max_iterations=3)
    
    print("="*70)
    print("Literature Review Summary")
    print("="*70 + "\n")
    print(result['synthesis'][:600] + "...\n")


def example_3_multi_source_synthesis():
    """Example 3: Multi-Source Information Synthesis"""
    print("\n" + "="*70)
    print("Example 3: Multi-Source Information Synthesis")
    print("="*70 + "\n")
    
    agent = ResearchAgent(collection_name="example_synthesis")
    
    # Add information from different sources
    sources = {
        "news_article": "Recent studies show AI adoption increasing by 40% in healthcare.",
        "research_paper": "AI diagnostic systems achieve 95% accuracy in medical imaging.",
        "industry_report": "Healthcare AI market expected to reach $45B by 2026.",
        "expert_opinion": "AI will transform healthcare but requires careful regulation.",
    }
    
    for source_type, content in sources.items():
        agent.add_knowledge(content, source=source_type)
    
    # Synthesize information
    query = "What is the impact of AI on healthcare?"
    
    print(f"Query: {query}\n")
    print("Synthesizing from multiple sources...\n")
    
    answer = agent.rag_agent.query(query, n_results=4, include_sources=True)
    
    print("="*70)
    print("Synthesized Answer")
    print("="*70 + "\n")
    print(answer + "\n")


def example_4_iterative_research():
    """Example 4: Iterative Research Refinement"""
    print("\n" + "="*70)
    print("Example 4: Iterative Research Refinement")
    print("="*70 + "\n")
    
    agent = ResearchAgent(collection_name="example_iterative")
    
    # Initial broad query
    initial_query = "What are neural networks?"
    
    print(f"Initial Query: {initial_query}")
    print("="*50 + "\n")
    
    # First iteration
    agent.add_knowledge(
        "Neural networks are computing systems inspired by biological brains.",
        source="basic"
    )
    
    answer1 = agent.quick_answer(initial_query)
    print(f"Answer 1:\n{answer1[:200]}...\n")
    
    # Refine query based on initial answer
    refined_query = "What are the different types of neural network architectures?"
    
    print(f"\nRefined Query: {refined_query}")
    print("="*50 + "\n")
    
    # Add more detailed knowledge
    agent.add_knowledge(
        "Common neural network types include CNNs for images, RNNs for sequences, and Transformers for NLP.",
        source="detailed"
    )
    
    answer2 = agent.quick_answer(refined_query)
    print(f"Answer 2:\n{answer2[:200]}...\n")
    
    # Further refinement
    specific_query = "How do Transformers differ from RNNs?"
    
    print(f"\nSpecific Query: {specific_query}")
    print("="*50 + "\n")
    
    agent.add_knowledge(
        "Transformers use self-attention mechanisms and process sequences in parallel, unlike sequential RNNs.",
        source="specific"
    )
    
    answer3 = agent.quick_answer(specific_query)
    print(f"Answer 3:\n{answer3[:200]}...\n")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("RAG Agent - Advanced Examples")
    print("="*70 + "\n")
    
    examples = [
        ("Competitive Analysis", example_1_competitive_analysis),
        ("Literature Review", example_2_literature_review),
        ("Multi-Source Synthesis", example_3_multi_source_synthesis),
        ("Iterative Research", example_4_iterative_research),
    ]
    
    for i, (name, example_func) in enumerate(examples, 1):
        print(f"\n[{i}/{len(examples)}] Running: {name}")
        
        try:
            example_func()
        except Exception as e:
            print(f"Error in example: {e}\n")
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print("\n" + "="*70)
    print("All Examples Complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
