"""
Vector Store Manager using ChromaDB
"""
import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import uuid

load_dotenv()


class VectorStore:
    """Manages vector embeddings and similarity search using ChromaDB"""
    
    def __init__(
        self, 
        collection_name: Optional[str] = None,
        persist_directory: Optional[str] = None,
        embedding_model: Optional[str] = None
    ):
        """
        Initialize vector store
        
        Args:
            collection_name: Name of the collection
            persist_directory: Directory to persist database
            embedding_model: Name of the embedding model
        """
        self.collection_name = collection_name or os.getenv("COLLECTION_NAME", "research_documents")
        self.persist_directory = persist_directory or os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Initialize embedding model
        model_name = embedding_model or os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.embedding_model = SentenceTransformer(model_name)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "Research documents and context"}
        )
        
        print(f"✓ Vector store initialized: {self.collection_name}")
        print(f"✓ Documents in collection: {self.collection.count()}")
    
    def add_documents(
        self, 
        documents: List[str], 
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to vector store
        
        Args:
            documents: List of text documents
            metadatas: Optional metadata for each document
            ids: Optional IDs for documents
            
        Returns:
            List of document IDs
        """
        if not documents:
            return []
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents).tolist()
        
        # Prepare metadata
        if metadatas is None:
            metadatas = [{"source": "unknown"} for _ in documents]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✓ Added {len(documents)} documents to vector store")
        return ids
    
    def search(
        self, 
        query: str, 
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Search for similar documents
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            Dictionary with documents, distances, and metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )
        
        return {
            "documents": results["documents"][0] if results["documents"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "ids": results["ids"][0] if results["ids"] else []
        }
    
    def get_context_for_query(self, query: str, n_results: int = 5) -> str:
        """
        Get formatted context for a query
        
        Args:
            query: Search query
            n_results: Number of results to retrieve
            
        Returns:
            Formatted context string
        """
        results = self.search(query, n_results)
        
        if not results["documents"]:
            return "No relevant context found."
        
        context_parts = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results["documents"], 
            results["metadatas"], 
            results["distances"]
        ), 1):
            source = metadata.get("source", "Unknown")
            relevance = 1 - distance  # Convert distance to similarity score
            
            context_parts.append(
                f"[Source {i}: {source} (Relevance: {relevance:.2f})]\n{doc}\n"
            )
        
        return "\n".join(context_parts)
    
    def delete_collection(self):
        """Delete the entire collection"""
        self.client.delete_collection(name=self.collection_name)
        print(f"✓ Deleted collection: {self.collection_name}")
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        count = self.collection.count()
        
        return {
            "name": self.collection_name,
            "document_count": count,
            "persist_directory": self.persist_directory
        }
    
    def update_document(self, doc_id: str, document: str, metadata: Optional[Dict] = None):
        """
        Update an existing document
        
        Args:
            doc_id: Document ID to update
            document: New document text
            metadata: New metadata
        """
        embedding = self.embedding_model.encode([document])[0].tolist()
        
        self.collection.update(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[document],
            metadatas=[metadata] if metadata else None
        )
        
        print(f"✓ Updated document: {doc_id}")
    
    def delete_documents(self, ids: List[str]):
        """
        Delete documents by IDs
        
        Args:
            ids: List of document IDs to delete
        """
        self.collection.delete(ids=ids)
        print(f"✓ Deleted {len(ids)} documents")


if __name__ == "__main__":
    # Test the vector store
    vs = VectorStore()
    
    # Add test documents
    docs = [
        "RAG stands for Retrieval-Augmented Generation, combining retrieval and generation.",
        "Vector databases store embeddings for efficient similarity search.",
        "AI agents can autonomously perform tasks and make decisions."
    ]
    
    ids = vs.add_documents(
        documents=docs,
        metadatas=[{"source": "test"} for _ in docs]
    )
    
    # Search
    results = vs.search("What is RAG?", n_results=2)
    print("\nSearch Results:")
    for doc in results["documents"]:
        print(f"- {doc}")
    
    # Get stats
    stats = vs.get_collection_stats()
    print(f"\nCollection Stats: {stats}")
