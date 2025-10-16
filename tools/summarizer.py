"""
Text Summarization Tool
"""
from typing import List, Optional, Dict
from utils.llm_client import LLMClient


class SummarizerTool:
    """Tool for summarizing text content"""
    
    def __init__(self):
        self.llm = LLMClient()
    
    def summarize(
        self, 
        text: str, 
        style: str = "comprehensive",
        max_words: int = 300
    ) -> str:
        """
        Summarize text
        
        Args:
            text: Text to summarize
            style: Summary style (comprehensive, concise, bullet)
            max_words: Maximum words in summary
            
        Returns:
            Summary text
        """
        if style == "bullet":
            prompt = f"""Create a bullet-point summary of the following text.
            Extract the {max_words // 20} most important points.

Text:
{text}

Bullet Summary:"""
        elif style == "concise":
            prompt = f"""Create a concise summary of the following text in no more than {max_words} words.
            Focus only on the most critical information.

Text:
{text}

Concise Summary:"""
        else:  # comprehensive
            prompt = f"""Create a comprehensive summary of the following text in approximately {max_words} words.
            Include key details, main arguments, and important conclusions.

Text:
{text}

Comprehensive Summary:"""
        
        return self.llm.generate(prompt, temperature=0.5, max_tokens=1024)
    
    def extract_insights(self, text: str) -> Dict:
        """
        Extract key insights from text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with insights
        """
        prompt = f"""Analyze the following text and extract:
1. Main Topic (one sentence)
2. Key Points (3-5 bullet points)
3. Important Conclusions (2-3 sentences)
4. Actionable Insights (if any)

Text:
{text}

Analysis:"""
        
        response = self.llm.generate(prompt, temperature=0.3)
        
        return {
            "analysis": response,
            "raw_text_length": len(text)
        }
    
    def compare_documents(self, doc1: str, doc2: str) -> str:
        """
        Compare two documents
        
        Args:
            doc1: First document
            doc2: Second document
            
        Returns:
            Comparison analysis
        """
        prompt = f"""Compare and contrast the following two documents:

Document 1:
{doc1}

Document 2:
{doc2}

Please provide:
1. Common themes and agreements
2. Key differences
3. Unique points in each document
4. Overall synthesis

Comparison:"""
        
        return self.llm.generate(prompt, temperature=0.4, max_tokens=2048)
    
    def synthesize_multiple_sources(self, sources: List[str]) -> str:
        """
        Synthesize information from multiple sources
        
        Args:
            sources: List of source texts
            
        Returns:
            Synthesized summary
        """
        # Combine sources with labels
        combined_text = ""
        for i, source in enumerate(sources, 1):
            combined_text += f"\n\n--- Source {i} ---\n{source}"
        
        prompt = f"""Synthesize the information from the following {len(sources)} sources into a coherent summary.
        Identify common themes, resolve contradictions, and provide a comprehensive overview.

{combined_text}

Synthesized Summary:"""
        
        return self.llm.generate(prompt, temperature=0.5, max_tokens=2048)
    
    def answer_from_context(self, question: str, context: str) -> str:
        """
        Answer a question based on provided context
        
        Args:
            question: Question to answer
            context: Context containing relevant information
            
        Returns:
            Answer
        """
        return self.llm.analyze_with_context(question, context)


if __name__ == "__main__":
    # Test summarizer
    summarizer = SummarizerTool()
    
    sample_text = """
    Artificial Intelligence (AI) is revolutionizing various industries by enabling 
    machines to perform tasks that typically require human intelligence. Machine learning, 
    a subset of AI, allows systems to learn from data and improve their performance over time. 
    Deep learning, which uses neural networks with multiple layers, has led to breakthroughs 
    in image recognition, natural language processing, and autonomous systems. Companies are 
    increasingly adopting AI to enhance efficiency, reduce costs, and create innovative products.
    """
    
    print("Comprehensive Summary:")
    print(summarizer.summarize(sample_text, style="comprehensive", max_words=50))
    
    print("\n" + "="*50)
    print("Bullet Summary:")
    print(summarizer.summarize(sample_text, style="bullet", max_words=100))
