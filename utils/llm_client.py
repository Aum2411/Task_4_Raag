"""
LLM Client wrapper for Groq API
"""
import os
from groq import Groq
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()


class LLMClient:
    """Wrapper for Groq API client with enhanced functionality"""
    
    def __init__(self, model: Optional[str] = None):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False
    ) -> str:
        """
        Generate chat completion
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response
            
        Returns:
            Generated text response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
            
            if stream:
                return response  # Return generator for streaming
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in chat completion: {e}")
            raise
    
    def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        Simple text generation
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        return self.chat_completion(messages, temperature, max_tokens)
    
    def analyze_with_context(
        self, 
        query: str, 
        context: str,
        instruction: Optional[str] = None
    ) -> str:
        """
        Analyze query with provided context
        
        Args:
            query: User query
            context: Relevant context/documents
            instruction: Optional specific instruction
            
        Returns:
            Analysis result
        """
        system_prompt = instruction or """You are a helpful research assistant. 
        Use the provided context to answer questions accurately and comprehensively. 
        Always cite sources when available."""
        
        prompt = f"""Context:
{context}

Question: {query}

Please provide a detailed answer based on the context above."""
        
        return self.generate(prompt, system_prompt=system_prompt)
    
    def summarize(self, text: str, max_length: int = 500) -> str:
        """
        Summarize text
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summary
        """
        prompt = f"""Summarize the following text in approximately {max_length} words. 
        Focus on key points and main ideas.

Text:
{text}

Summary:"""
        
        return self.generate(prompt, temperature=0.5, max_tokens=1024)
    
    def extract_key_points(self, text: str, num_points: int = 5) -> List[str]:
        """
        Extract key points from text
        
        Args:
            text: Text to analyze
            num_points: Number of key points to extract
            
        Returns:
            List of key points
        """
        prompt = f"""Extract the {num_points} most important key points from the following text.
        Return them as a numbered list.

Text:
{text}

Key Points:"""
        
        response = self.generate(prompt, temperature=0.3)
        
        # Parse response into list
        lines = response.strip().split('\n')
        points = [line.strip() for line in lines if line.strip() and any(c.isalnum() for c in line)]
        
        return points[:num_points]


if __name__ == "__main__":
    # Test the client
    client = LLMClient()
    
    response = client.generate("Explain what a RAG agent is in one paragraph.")
    print("Response:", response)
