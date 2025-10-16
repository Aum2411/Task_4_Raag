"""
Web Search Tool using Serper API
"""
import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class WebSearchTool:
    """Web search tool using Serper API for Google search results"""
    
    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        if not self.api_key:
            raise ValueError("SERPER_API_KEY not found in environment variables")
        
        self.base_url = "https://google.serper.dev/search"
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
    
    def search(
        self, 
        query: str, 
        num_results: int = 10,
        search_type: str = "search"
    ) -> Dict:
        """
        Perform web search
        
        Args:
            query: Search query
            num_results: Number of results to return
            search_type: Type of search (search, news, images)
            
        Returns:
            Search results dictionary
        """
        payload = {
            "q": query,
            "num": num_results
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error performing search: {e}")
            return {"organic": [], "error": str(e)}
    
    def get_search_results(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Get formatted search results
        
        Args:
            query: Search query
            num_results: Number of results
            
        Returns:
            List of result dictionaries
        """
        results = self.search(query, num_results)
        
        if "error" in results:
            return []
        
        organic_results = results.get("organic", [])
        
        formatted_results = []
        for result in organic_results[:num_results]:
            formatted_results.append({
                "title": result.get("title", ""),
                "link": result.get("link", ""),
                "snippet": result.get("snippet", ""),
                "date": result.get("date", "")
            })
        
        return formatted_results
    
    def search_and_summarize(self, query: str, num_results: int = 5) -> str:
        """
        Search and create a summary of results
        
        Args:
            query: Search query
            num_results: Number of results
            
        Returns:
            Formatted summary string
        """
        results = self.get_search_results(query, num_results)
        
        if not results:
            return "No search results found."
        
        summary_parts = [f"Search Results for: '{query}'\n"]
        
        for i, result in enumerate(results, 1):
            summary_parts.append(f"\n{i}. {result['title']}")
            summary_parts.append(f"   URL: {result['link']}")
            summary_parts.append(f"   {result['snippet']}")
            if result.get('date'):
                summary_parts.append(f"   Date: {result['date']}")
        
        return "\n".join(summary_parts)
    
    def get_answer_box(self, query: str) -> Optional[str]:
        """
        Get answer box if available
        
        Args:
            query: Search query
            
        Returns:
            Answer box content or None
        """
        results = self.search(query, num_results=1)
        
        answer_box = results.get("answerBox", {})
        
        if answer_box:
            answer = answer_box.get("answer") or answer_box.get("snippet")
            return answer
        
        return None
    
    def get_related_searches(self, query: str) -> List[str]:
        """
        Get related search queries
        
        Args:
            query: Search query
            
        Returns:
            List of related queries
        """
        results = self.search(query, num_results=5)
        
        related = results.get("relatedSearches", [])
        
        return [item.get("query", "") for item in related if item.get("query")]


class WebScraperTool:
    """Simple web scraper for extracting content from URLs"""
    
    @staticmethod
    def scrape_url(url: str, timeout: int = 10) -> Optional[str]:
        """
        Scrape content from URL
        
        Args:
            url: URL to scrape
            timeout: Request timeout
            
        Returns:
            Extracted text content
        """
        try:
            from bs4 import BeautifulSoup
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator='\n', strip=True)
            
            # Clean up
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = '\n'.join(lines)
            
            return text
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    @staticmethod
    def scrape_multiple_urls(urls: List[str]) -> Dict[str, str]:
        """
        Scrape multiple URLs
        
        Args:
            urls: List of URLs
            
        Returns:
            Dictionary mapping URLs to content
        """
        results = {}
        
        for url in urls:
            content = WebScraperTool.scrape_url(url)
            if content:
                results[url] = content
        
        return results


if __name__ == "__main__":
    # Test web search
    search_tool = WebSearchTool()
    
    print("Testing Web Search...")
    results = search_tool.get_search_results("What are AI agents?", num_results=3)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   {result['snippet']}")
    
    print("\n" + "="*50)
    print("Search Summary:")
    summary = search_tool.search_and_summarize("RAG systems", num_results=3)
    print(summary)
