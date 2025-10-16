# RAG Agent for Deep Research & Task Delegation

A sophisticated Retrieval-Augmented Generation (RAG) agent system designed for complex research activities, intelligent task delegation, and multi-step workflow orchestration.

## 🌟 Features

- **Intelligent RAG System**: Vector database-powered document retrieval using ChromaDB
- **Web Search Integration**: Real-time web search using Serper API
- **Task Delegation**: Automatic breaking down of complex prompts into subtasks
- **Workflow Orchestration**: Multi-step research workflows with dependency management
- **Document Processing**: Support for PDF, DOCX, TXT, and web content
- **Smart Summarization**: Context-aware document summarization
- **Research Synthesis**: Combines multiple sources into coherent insights

## 🔑 APIs Used

1. **Groq API**: Fast LLM inference (Llama 3.1 70B)
2. **Serper API**: Real-time Google search results
3. **Sentence Transformers**: Local embeddings (no API needed)

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

```bash
# Run the RAG agent
python main.py

# Or use specific modes
python main.py --mode research --query "Explain quantum computing applications"
python main.py --mode document --path "./docs/research_paper.pdf"
```

## 🏗️ Architecture

```
├── main.py                 # Main application entry point
├── agents/
│   ├── rag_agent.py       # Core RAG agent implementation
│   ├── research_agent.py  # Research orchestration logic
│   └── task_delegator.py  # Task decomposition & delegation
├── tools/
│   ├── web_search.py      # Serper API integration
│   ├── document_loader.py # Document processing utilities
│   └── summarizer.py      # Text summarization tools
├── workflows/
│   └── research_workflow.py # Multi-step research workflows
└── utils/
    ├── vector_store.py    # ChromaDB vector database manager
    └── llm_client.py      # Groq API client wrapper
```

## 💡 Usage Examples

### Basic Research Query
```python
from agents.rag_agent import RAGAgent

agent = RAGAgent()
result = agent.research("What are the latest developments in AI agents?")
print(result)
```

### Complex Task Delegation
```python
from agents.research_agent import ResearchAgent

agent = ResearchAgent()
result = agent.deep_research(
    "Compare different approaches to building autonomous agents, "
    "analyze their strengths and weaknesses, and provide recommendations"
)
```

## 🔧 Configuration

Edit `.env` file to configure:
- API keys
- Model selection
- Vector database settings
- Agent parameters

## 📊 Workflow Examples

1. **Document Analysis**: Upload → Chunk → Embed → Store → Query
2. **Web Research**: Query → Search → Scrape → Summarize → Synthesize
3. **Complex Research**: Decompose → Delegate → Execute → Aggregate → Report

## 🛠️ Advanced Features

- **Adaptive Context Window**: Dynamically adjusts retrieval based on query complexity
- **Source Attribution**: Tracks and cites all information sources
- **Iterative Refinement**: Self-improves answers through reflection
- **Multi-modal Support**: Handles text, documents, and web content

## 📝 License

MIT License
