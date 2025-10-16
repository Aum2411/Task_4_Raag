"""
Task Delegator Agent - Breaks down complex tasks into subtasks
"""
from typing import List, Dict
from utils.llm_client import LLMClient


class TaskDelegator:
    """Intelligently breaks down complex tasks into manageable subtasks"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def decompose_task(self, task: str) -> List[Dict]:
        """
        Decompose a complex task into subtasks
        
        Args:
            task: Complex task description
            
        Returns:
            List of subtask dictionaries
        """
        system_prompt = """You are an expert task planner. Break down complex tasks into 
        logical, sequential subtasks. Each subtask should be specific and actionable."""
        
        prompt = f"""Analyze the following complex task and break it down into 3-7 specific subtasks.

Task: {task}

For each subtask, provide:
1. A clear title
2. A brief description
3. The type of action needed (research, analyze, synthesize, compare, summarize)
4. Dependencies (if any)

Format your response as a numbered list with these details for each subtask.

Subtasks:"""
        
        response = self.llm.generate(prompt, system_prompt=system_prompt, temperature=0.3)
        
        # Parse response into structured format
        subtasks = self._parse_subtasks(response)
        
        return subtasks
    
    def _parse_subtasks(self, response: str) -> List[Dict]:
        """Parse LLM response into structured subtasks"""
        subtasks = []
        lines = response.strip().split('\n')
        
        current_task = {}
        task_counter = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_task:
                    current_task['id'] = task_counter
                    subtasks.append(current_task)
                    current_task = {}
                    task_counter += 1
                continue
            
            # Check if it's a numbered item (new task)
            if line[0].isdigit() and '.' in line[:3]:
                if current_task:
                    current_task['id'] = task_counter
                    subtasks.append(current_task)
                    task_counter += 1
                
                title = line.split('.', 1)[1].strip()
                current_task = {
                    'title': title,
                    'description': '',
                    'action_type': 'research',
                    'dependencies': []
                }
            else:
                # Add to current task description
                if current_task:
                    if 'description' in current_task:
                        current_task['description'] += ' ' + line
        
        # Add last task
        if current_task:
            current_task['id'] = task_counter
            subtasks.append(current_task)
        
        return subtasks
    
    def prioritize_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """
        Prioritize tasks based on dependencies and importance
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            Prioritized task list
        """
        # Simple priority: tasks with no dependencies first
        no_deps = [t for t in tasks if not t.get('dependencies')]
        with_deps = [t for t in tasks if t.get('dependencies')]
        
        return no_deps + with_deps
    
    def create_research_plan(self, query: str) -> Dict:
        """
        Create a comprehensive research plan
        
        Args:
            query: Research query
            
        Returns:
            Research plan dictionary
        """
        prompt = f"""Create a detailed research plan for the following query:

Query: {query}

Provide:
1. Main Research Objective (1-2 sentences)
2. Key Questions to Answer (3-5 questions)
3. Information Sources Needed (web search, documents, databases, etc.)
4. Research Steps (sequential steps to follow)
5. Expected Deliverables (what the final output should contain)

Research Plan:"""
        
        response = self.llm.generate(prompt, temperature=0.3)
        
        return {
            "query": query,
            "plan": response,
            "subtasks": self.decompose_task(query)
        }
    
    def identify_task_type(self, task: str) -> str:
        """
        Identify the type of task
        
        Args:
            task: Task description
            
        Returns:
            Task type (research, analysis, comparison, synthesis, etc.)
        """
        task_lower = task.lower()
        
        if any(word in task_lower for word in ['compare', 'contrast', 'difference']):
            return 'comparison'
        elif any(word in task_lower for word in ['analyze', 'examine', 'evaluate']):
            return 'analysis'
        elif any(word in task_lower for word in ['summarize', 'overview', 'brief']):
            return 'summarization'
        elif any(word in task_lower for word in ['combine', 'synthesize', 'integrate']):
            return 'synthesis'
        else:
            return 'research'
    
    def estimate_complexity(self, task: str) -> str:
        """
        Estimate task complexity
        
        Args:
            task: Task description
            
        Returns:
            Complexity level (simple, moderate, complex)
        """
        subtasks = self.decompose_task(task)
        num_subtasks = len(subtasks)
        
        if num_subtasks <= 3:
            return 'simple'
        elif num_subtasks <= 5:
            return 'moderate'
        else:
            return 'complex'


if __name__ == "__main__":
    # Test task delegator
    delegator = TaskDelegator()
    
    complex_task = """Compare different approaches to building AI agents, 
    analyze their strengths and weaknesses, and provide recommendations for 
    specific use cases"""
    
    print("Decomposing complex task...")
    subtasks = delegator.decompose_task(complex_task)
    
    print(f"\nFound {len(subtasks)} subtasks:")
    for task in subtasks:
        print(f"\n{task['id']}. {task['title']}")
        print(f"   Description: {task['description'][:100]}...")
    
    print("\n" + "="*50)
    print("Creating research plan...")
    plan = delegator.create_research_plan("What is the future of quantum computing?")
    print(f"\nPlan: {plan['plan'][:200]}...")
