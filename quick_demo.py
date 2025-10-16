"""
Quick Demo - RAG Agent in Action
"""
from agents.research_agent import ResearchAgent
from colorama import init, Fore, Style

init(autoreset=True)

print(f"\n{Fore.CYAN}{'='*70}")
print("RAG Agent - Quick Demo")
print(f"{'='*70}{Style.RESET_ALL}\n")

# Initialize agent
print("Initializing RAG Agent...")
agent = ResearchAgent(collection_name="quick_demo")

# Add some knowledge
print(f"\n{Fore.GREEN}Step 1: Adding knowledge to the system...{Style.RESET_ALL}")
knowledge = [
    "RAG (Retrieval-Augmented Generation) combines retrieval and generation for better AI responses.",
    "Vector databases like ChromaDB enable semantic search using embeddings.",
    "AI agents are autonomous systems that can perceive and act to achieve goals.",
    "Task delegation in AI involves breaking complex tasks into smaller, manageable subtasks.",
]

for i, k in enumerate(knowledge, 1):
    agent.add_knowledge(k, source=f"knowledge_{i}")

print(f"✓ Added {len(knowledge)} knowledge items\n")

# Quick Answer
print(f"{Fore.GREEN}Step 2: Testing Quick Answer...{Style.RESET_ALL}")
question = "What is RAG and how does it work?"
print(f"Question: {question}\n")

answer = agent.quick_answer(question)
print(f"{Fore.YELLOW}Answer:{Style.RESET_ALL}")
print(answer[:400] + "...\n")

# Task Delegation Demo
print(f"{Fore.GREEN}Step 3: Testing Task Delegation...{Style.RESET_ALL}")
complex_query = "Analyze the benefits of using RAG systems in AI applications"
print(f"Complex Query: {complex_query}\n")

plan = agent.task_delegator.create_research_plan(complex_query)
print(f"Created research plan with {len(plan['subtasks'])} subtasks:")
for i, task in enumerate(plan['subtasks'][:3], 1):
    print(f"  {i}. {task['title']}")
print()

# Compare Topics
print(f"{Fore.GREEN}Step 4: Comparing Topics...{Style.RESET_ALL}")
print("Comparing: RAG vs Traditional LLMs\n")

comparison = agent.compare_topics("RAG systems", "Traditional LLMs")
print(f"{Fore.YELLOW}Comparison Result:{Style.RESET_ALL}")
print(comparison['comparison'][:400] + "...\n")

print(f"{Fore.CYAN}{'='*70}")
print("✓ Demo Complete!")
print(f"{'='*70}{Style.RESET_ALL}\n")

print(f"{Fore.GREEN}Your RAG agent is working perfectly!{Style.RESET_ALL}")
print(f"\nTry these commands:")
print(f"  python main.py                    # Interactive mode")
print(f"  python main.py --mode research --query \"Your question\"")
print(f"  python examples.py                # See advanced examples")
