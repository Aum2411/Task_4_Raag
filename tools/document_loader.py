"""
Document Loader for various file formats
"""
import os
from typing import List, Dict, Optional
from pathlib import Path


class DocumentLoader:
    """Load and process documents from various formats"""
    
    @staticmethod
    def load_text_file(file_path: str) -> str:
        """
        Load text file
        
        Args:
            file_path: Path to text file
            
        Returns:
            File content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading text file {file_path}: {e}")
            return ""
    
    @staticmethod
    def load_pdf(file_path: str) -> str:
        """
        Load PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(file_path)
            text_parts = []
            
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            return "\n".join(text_parts)
            
        except Exception as e:
            print(f"Error loading PDF {file_path}: {e}")
            return ""
    
    @staticmethod
    def load_docx(file_path: str) -> str:
        """
        Load DOCX file
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text
        """
        try:
            from docx import Document
            
            doc = Document(file_path)
            text_parts = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            return "\n".join(text_parts)
            
        except Exception as e:
            print(f"Error loading DOCX {file_path}: {e}")
            return ""
    
    @staticmethod
    def load_document(file_path: str) -> str:
        """
        Auto-detect and load document
        
        Args:
            file_path: Path to document
            
        Returns:
            Extracted text
        """
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return ""
        
        ext = Path(file_path).suffix.lower()
        
        if ext == '.pdf':
            return DocumentLoader.load_pdf(file_path)
        elif ext == '.docx':
            return DocumentLoader.load_docx(file_path)
        elif ext in ['.txt', '.md', '.py', '.js', '.json', '.xml', '.csv']:
            return DocumentLoader.load_text_file(file_path)
        else:
            print(f"Unsupported file format: {ext}")
            return ""
    
    @staticmethod
    def chunk_text(
        text: str, 
        chunk_size: int = 1000, 
        chunk_overlap: int = 200
    ) -> List[str]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Text to chunk
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            
            # Try to break at sentence boundaries
            if end < text_length:
                # Look for sentence endings
                chunk = text[start:end]
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                
                break_point = max(last_period, last_newline)
                if break_point > chunk_size * 0.5:  # At least 50% of chunk size
                    end = start + break_point + 1
            
            chunks.append(text[start:end].strip())
            start = end - chunk_overlap
        
        return chunks
    
    @staticmethod
    def load_and_chunk_document(
        file_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> List[Dict]:
        """
        Load document and split into chunks with metadata
        
        Args:
            file_path: Path to document
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        text = DocumentLoader.load_document(file_path)
        
        if not text:
            return []
        
        chunks = DocumentLoader.chunk_text(text, chunk_size, chunk_overlap)
        
        filename = os.path.basename(file_path)
        
        return [
            {
                "text": chunk,
                "metadata": {
                    "source": filename,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            }
            for i, chunk in enumerate(chunks)
        ]
    
    @staticmethod
    def load_directory(
        directory_path: str,
        extensions: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Load all documents from a directory
        
        Args:
            directory_path: Path to directory
            extensions: List of file extensions to include
            
        Returns:
            List of document dictionaries
        """
        if extensions is None:
            extensions = ['.txt', '.pdf', '.docx', '.md']
        
        documents = []
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    chunks = DocumentLoader.load_and_chunk_document(file_path)
                    documents.extend(chunks)
        
        return documents


if __name__ == "__main__":
    # Test document loader
    loader = DocumentLoader()
    
    # Test text chunking
    sample_text = "This is a test sentence. " * 100
    chunks = loader.chunk_text(sample_text, chunk_size=100, chunk_overlap=20)
    
    print(f"Created {len(chunks)} chunks from sample text")
    print(f"First chunk: {chunks[0][:50]}...")
