"""
Core RAG Agent - Retrieval-Augmented Generation
"""
from typing import List, Dict, Optional
from utils.llm_client import LLMClient
from utils.vector_store import VectorStore
from tools.document_loader import DocumentLoader
import os


class RAGAgent:
    """
    Core RAG agent that combines retrieval and generation
    """
    
    def __init__(
        self, 
        collection_name: Optional[str] = None,
        auto_load_docs: bool = False
    ):
        """
        Initialize RAG agent
        
        Args:
            collection_name: Name for vector store collection
            auto_load_docs: Whether to auto-load documents from ./documents
        """
        self.llm = LLMClient()
        self.vector_store = VectorStore(collection_name=collection_name)
        self.document_loader = DocumentLoader()
        
        if auto_load_docs:
            self._auto_load_documents()
        
        print("✓ RAG Agent initialized")
    
    def _auto_load_documents(self):
        """Auto-load documents from ./documents directory"""
        docs_dir = "./documents"
        if os.path.exists(docs_dir):
            documents = self.document_loader.load_directory(docs_dir)
            if documents:
                self.add_documents([d['text'] for d in documents], 
                                 [d['metadata'] for d in documents])
                print(f"✓ Auto-loaded {len(documents)} document chunks")
    
    def add_documents(
        self, 
        documents: List[str], 
        metadatas: Optional[List[Dict]] = None
    ) -> List[str]:
        """
        Add documents to the knowledge base
        
        Args:
            documents: List of document texts
            metadatas: Optional metadata for each document
            
        Returns:
            List of document IDs
        """
        return self.vector_store.add_documents(documents, metadatas)
    
    def add_document_file(self, file_path: str) -> int:
        """
        Add a document file to knowledge base
        
        Args:
            file_path: Path to document file
            
        Returns:
            Number of chunks added
        """
        chunks = self.document_loader.load_and_chunk_document(file_path)
        
        if not chunks:
            print(f"No content extracted from {file_path}")
            return 0
        
        documents = [chunk['text'] for chunk in chunks]
        metadatas = [chunk['metadata'] for chunk in chunks]
        
        self.add_documents(documents, metadatas)
        
        return len(chunks)
    
    def query(
        self, 
        question: str, 
        n_results: int = 5,
        include_sources: bool = True
    ) -> str:
        """
        Query the RAG system
        
        Args:
            question: User question
            n_results: Number of context documents to retrieve
            include_sources: Whether to include source citations
            
        Returns:
            Generated answer
        """
        # Retrieve relevant context
        context = self.vector_store.get_context_for_query(question, n_results)
        
        if context == "No relevant context found.":
            # Fallback to direct generation
            return self.llm.generate(
                f"Answer this question to the best of your knowledge: {question}"
            )
        
        # Generate answer with context
        instruction = """You are a knowledgeable research assistant. 
        Use the provided context to answer questions accurately and comprehensively.
        If the context doesn't contain enough information, say so clearly.
        Always cite sources using [Source X] notation when referencing information."""
        
        answer = self.llm.analyze_with_context(question, context, instruction)
        
        if include_sources:
            answer += "\n\n---\n[Context retrieved from knowledge base]"
        
        return answer
    
    def research(
        self, 
        topic: str, 
        depth: str = "comprehensive"
    ) -> Dict:
        """
        Perform research on a topic
        
        Args:
            topic: Research topic
            depth: Level of depth (quick, standard, comprehensive)
            
        Returns:
            Research results dictionary
        """
        # Determine number of sources based on depth
        n_results = {
            'quick': 3,
            'standard': 5,
            'comprehensive': 10
        }.get(depth, 5)
        
        # Retrieve relevant information
        search_results = self.vector_store.search(topic, n_results=n_results)
        
        if not search_results['documents']:
            return {
                'topic': topic,
                'answer': 'No relevant information found in knowledge base.',
                'sources': []
            }
        
        # Generate comprehensive research summary
        context = self.vector_store.get_context_for_query(topic, n_results)
        
        prompt = f"""Based on the following context, provide a comprehensive research summary about: {topic}

Context:
{context}

Provide:
1. Overview (2-3 paragraphs)
2. Key Points (bullet points)
3. Important Details
4. Conclusions/Implications

Research Summary:"""
        
        summary = self.llm.generate(prompt, temperature=0.5, max_tokens=2048)
        
        return {
            'topic': topic,
            'summary': summary,
            'num_sources': len(search_results['documents']),
            'sources': [
                {
                    'text': doc[:200] + '...',
                    'metadata': meta,
                    'relevance': 1 - dist
                }
                for doc, meta, dist in zip(
                    search_results['documents'],
                    search_results['metadatas'],
                    search_results['distances']
                )
            ]
        }
    
    def chat(self, message: str, conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Chat with context awareness
        
        Args:
            message: User message
            conversation_history: Optional conversation history
            
        Returns:
            Response
        """
        # Get relevant context
        context = self.vector_store.get_context_for_query(message, n_results=3)
        
        # Build messages
        messages = []
        
        system_msg = f"""You are a helpful AI assistant with access to a knowledge base.
        Use the following context when relevant to answer questions:
        
        {context}
        """
        messages.append({"role": "system", "content": system_msg})
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history[-6:])  # Last 3 exchanges
        
        messages.append({"role": "user", "content": message})
        
        return self.llm.chat_completion(messages)
    
    def get_stats(self) -> Dict:
        """Get RAG agent statistics"""
        return self.vector_store.get_collection_stats()


if __name__ == "__main__":
    # Test RAG agent
    agent = RAGAgent(collection_name="test_collection")
    
    # Add sample documents
    docs = [
        "RAG (Retrieval-Augmented Generation) combines retrieval and generation for better AI responses.",
        "Vector databases store embeddings for efficient similarity search in RAG systems.",
        "ChromaDB is an open-source vector database designed for AI applications."
    ]
    
    agent.add_documents(docs, [{"source": "test"} for _ in docs])
    
    # Query
    print("\nQuerying RAG agent...")
    answer = agent.query("What is RAG?")
    print(f"\nAnswer: {answer}")
    
    # Research
    print("\n" + "="*50)
    print("Performing research...")
    research = agent.research("vector databases")
    print(f"\nResearch Summary:\n{research['summary'][:300]}...")
