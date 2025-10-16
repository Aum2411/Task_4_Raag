# 🎨 RAG Agent System Architecture Diagrams

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │ Interactive  │  │  Command     │  │   Python API         │ │
│  │     CLI      │  │   Line       │  │   (Programmatic)     │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MAIN APPLICATION                             │
│                      (main.py)                                  │
│  • Request routing                                              │
│  • Mode selection                                               │
│  • Output formatting                                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RESEARCH AGENT                                │
│              (agents/research_agent.py)                         │
│  • Deep research orchestration                                  │
│  • Multi-source coordination                                    │
│  • Result synthesis                                             │
└─────┬──────────────┬──────────────┬────────────────────────┬────┘
      │              │              │                        │
      ▼              ▼              ▼                        ▼
┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌────────────────┐
│   RAG    │  │   Task   │  │   Workflow   │  │  Summarizer   │
│  Agent   │  │ Delegator│  │    Engine    │  │     Tool      │
└────┬─────┘  └────┬─────┘  └──────┬───────┘  └───────┬────────┘
     │             │                │                   │
     │             │                │                   │
     ▼             ▼                ▼                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TOOLS LAYER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  Web Search  │  │   Document   │  │    Summarization     │ │
│  │   (Serper)   │  │    Loader    │  │      Engine          │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
     │                    │
     │                    │
     ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CORE UTILITIES                                │
│  ┌────────────────────────┐     ┌─────────────────────────┐   │
│  │    LLM Client          │     │    Vector Store         │   │
│  │    (Groq Wrapper)      │     │   (ChromaDB Manager)    │   │
│  └────────────────────────┘     └─────────────────────────┘   │
└──────────┬────────────────────────────────┬────────────────────┘
           │                                │
           ▼                                ▼
    ┌─────────────┐                  ┌──────────────┐
    │  Groq API   │                  │  ChromaDB    │
    │  (Cloud)    │                  │   (Local)    │
    └─────────────┘                  └──────────────┘
```

---

## Data Flow: Deep Research Query

```
    User Query: "Compare AI architectures"
              │
              ▼
    ┌─────────────────────┐
    │  Research Agent     │
    └─────────┬───────────┘
              │
              ▼
    ┌─────────────────────┐
    │  Task Delegator     │ ◄── Breaks into subtasks
    └─────────┬───────────┘
              │
              ├──► Subtask 1: Research transformers
              ├──► Subtask 2: Research CNNs
              ├──► Subtask 3: Research RNNs
              └──► Subtask 4: Compare & synthesize
              │
              ▼
    ┌──────────────────────────────────────┐
    │   Multi-Source Information Gathering │
    └──┬──────────────────────────┬────────┘
       │                          │
       ▼                          ▼
  ┌─────────┐              ┌──────────┐
  │   KB    │              │   Web    │
  │ Search  │              │  Search  │
  └────┬────┘              └────┬─────┘
       │                        │
       ▼                        ▼
  ┌─────────────────────────────────┐
  │  Vector Store Query Results     │
  │  • Document chunks              │
  │  • Relevance scores             │
  │  • Source metadata              │
  └────────────┬────────────────────┘
               │
               ▼
  ┌──────────────────────────────────┐
  │   Web Search Results             │
  │  • Search snippets               │
  │  • URLs                          │
  │  • Timestamps                    │
  └────────────┬─────────────────────┘
               │
               ▼
  ┌──────────────────────────────────┐
  │   Context Aggregation            │
  │  • Combine sources               │
  │  • Deduplicate                   │
  │  • Rank by relevance             │
  └────────────┬─────────────────────┘
               │
               ▼
  ┌──────────────────────────────────┐
  │   LLM Processing (Groq)          │
  │  • For each subtask:             │
  │    - Analyze context             │
  │    - Generate insights           │
  │    - Extract key points          │
  └────────────┬─────────────────────┘
               │
               ▼
  ┌──────────────────────────────────┐
  │   Synthesis & Report Generation  │
  │  • Combine subtask results       │
  │  • Identify patterns             │
  │  • Generate final report         │
  │  • Add source citations          │
  └────────────┬─────────────────────┘
               │
               ▼
  ┌──────────────────────────────────┐
  │   Return to User                 │
  │  • Final report                  │
  │  • Source list                   │
  │  • Execution summary             │
  └──────────────────────────────────┘
```

---

## RAG Pipeline Detail

```
    Document Input
         │
         ▼
┌─────────────────┐
│ Document Loader │
│  • PDF          │
│  • DOCX         │
│  • TXT          │
│  • MD           │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Chunking  │
│  • Split text   │
│  • Add overlap  │
│  • Preserve     │
│    context      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Embedding      │
│  Generation     │
│  (Sentence      │
│   Transformers) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Store in      │
│   ChromaDB      │
│  • Embeddings   │
│  • Text         │
│  • Metadata     │
└────────┬────────┘
         │
         │
    User Query ────────────────────┐
         │                         │
         ▼                         ▼
┌─────────────────┐       ┌────────────────┐
│ Query Embedding │       │  Query Text    │
│  (Sentence      │       │                │
│   Transformers) │       └────────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vector Search   │
│  • Similarity   │
│  • Top-K        │
│  • Filter       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Retrieve Docs   │
│  • Chunks       │
│  • Scores       │
│  • Sources      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Format Context  │
│  • Concatenate  │
│  • Add sources  │
│  • Structure    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Generate   │
│   (Groq API)    │
│  • Context      │
│  • Question     │
│  • Answer       │
└────────┬────────┘
         │
         ▼
    Final Answer
    with Sources
```

---

## Workflow Execution Flow

```
Workflow Definition
        │
        ▼
┌───────────────────┐
│  Add Steps        │
│  • step_id        │
│  • action         │
│  • dependencies   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Resolve Order     │
│  • Topological    │
│    sort           │
│  • Check cycles   │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Initialize        │
│ Context           │
│  • Shared state   │
│  • Results store  │
└────────┬──────────┘
         │
         ▼
    For Each Step
         │
         ├─► Check Dependencies
         │       │
         │       ├─► All Complete? ─Yes─┐
         │       │                       │
         │       └─► No ──► Skip Step    │
         │                               │
         ▼                               ▼
    ┌──────────────────┐         ┌──────────────┐
    │  Execute Step    │         │ Mark Skipped │
    │  • Run action    │         └──────────────┘
    │  • Pass context  │
    │  • Handle errors │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │  Store Result    │
    │  • In context    │
    │  • With step_id  │
    └────────┬─────────┘
             │
             ▼
    More Steps? ─Yes─┐
             │       │
             No      └─► Next Step
             │
             ▼
    ┌──────────────────┐
    │ Generate Summary │
    │  • Status        │
    │  • Results       │
    │  • Timing        │
    └────────┬─────────┘
             │
             ▼
    Return Results
```

---

## Component Interaction Matrix

```
┌────────────┬──────┬──────┬──────┬──────┬──────┬──────┐
│            │ RAG  │ Task │ Work │ Web  │ Doc  │ Sum  │
│            │Agent │ Delg │ Flow │Search│Loader│marize│
├────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│Research    │  ✓✓  │  ✓✓  │  ✓✓  │  ✓✓  │  ✓   │  ✓✓  │
│Agent       │      │      │      │      │      │      │
├────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│RAG Agent   │  --  │      │      │      │  ✓✓  │      │
├────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│Task        │      │  --  │      │      │      │      │
│Delegator   │      │      │      │      │      │      │
├────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│Workflow    │  ✓   │  ✓   │  --  │  ✓   │  ✓   │  ✓   │
│Engine      │      │      │      │      │      │      │
├────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│Web Search  │      │      │      │  --  │      │      │
├────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│Doc Loader  │  ✓   │      │      │      │  --  │      │
├────────────┼──────┼──────┼──────┼──────┼──────┼──────┤
│Summarizer  │  ✓   │      │      │      │      │  --  │
└────────────┴──────┴──────┴──────┴──────┴──────┴──────┘

Legend:
✓✓ = Strong dependency / Frequent use
✓  = Optional dependency / Occasional use
-- = Self (same component)
```

---

## API Call Flow

```
User Request
     │
     ▼
┌─────────────────────────────────────────┐
│         Application Layer               │
│  • Parse request                        │
│  • Route to handler                     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Agent Layer (Python)               │
│  • Orchestrate workflow                 │
│  • Manage state                         │
└─────┬─────────────────┬─────────────────┘
      │                 │
      │                 │
      ▼                 ▼
┌────────────┐    ┌────────────┐
│  Vector    │    │   Web      │
│  Search    │    │  Search    │
│  (Local)   │    │  (API)     │
└─────┬──────┘    └─────┬──────┘
      │                 │
      │                 │
      │                 ▼
      │          ┌────────────────┐
      │          │  Serper API    │
      │          │  HTTP Request  │
      │          └────────┬───────┘
      │                   │
      │                   ▼
      │          ┌────────────────┐
      │          │  Get Results   │
      │          │  • Snippets    │
      │          │  • URLs        │
      │          └────────┬───────┘
      │                   │
      │                   │
      ├───────────────────┘
      │
      ▼
┌──────────────────────────────┐
│  Aggregate Context           │
│  • Vector results            │
│  • Web results               │
│  • Format for LLM            │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Groq API Call               │
│  POST /chat/completions      │
│  {                           │
│    model: "llama-3.1-70b",   │
│    messages: [...],          │
│    temperature: 0.7          │
│  }                           │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Receive Response            │
│  • Generated text            │
│  • Token usage               │
│  • Timing info               │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Post-process                │
│  • Format output             │
│  • Add citations             │
│  • Clean text                │
└──────────┬───────────────────┘
           │
           ▼
    Return to User
```

---

## Error Handling Flow

```
    Operation Start
         │
         ▼
    Try Execute
         │
         ├────► Success ────► Return Result
         │
         └────► Exception
                    │
                    ▼
           ┌────────────────┐
           │  Error Type?   │
           └───┬────────────┘
               │
       ┌───────┼───────────────┐
       │       │               │
       ▼       ▼               ▼
   API Error   DB Error    Other Error
       │       │               │
       │       │               │
       ▼       ▼               ▼
   ┌────────┐ ┌────────┐  ┌────────┐
   │ Retry? │ │Recreate│  │  Log   │
   │ 3x max │ │  DB?   │  │ Error  │
   └───┬────┘ └───┬────┘  └───┬────┘
       │          │            │
       ├──► Yes ──┤            │
       │          │            │
       └──► No ───┤            │
                  │            │
                  ▼            ▼
         ┌──────────────────────┐
         │  Graceful Fallback   │
         │  • Return partial    │
         │  • Use cached        │
         │  • Notify user       │
         └──────────┬───────────┘
                    │
                    ▼
            Continue or Fail
```

---

## Performance Optimization Points

```
┌─────────────────────────────────────────┐
│         Performance Bottlenecks         │
└──────────────┬──────────────────────────┘
               │
       ┌───────┼───────┐
       │       │       │
       ▼       ▼       ▼
   ┌────┐  ┌────┐  ┌────┐
   │LLM │  │ DB │  │Net │
   │Call│  │I/O │  │I/O │
   └─┬──┘  └─┬──┘  └─┬──┘
     │       │       │
     │       │       │
     ▼       ▼       ▼
┌──────┐ ┌──────┐ ┌──────┐
│Cache │ │Index │ │Async │
│Results│ │ ing  │ │Calls │
└──────┘ └──────┘ └──────┘
     │       │       │
     └───────┼───────┘
             │
             ▼
    ┌────────────────┐
    │  Optimizations │
    │  • Batch calls │
    │  • Connection  │
    │    pooling     │
    │  • Result      │
    │    caching     │
    └────────────────┘
```

---

## Scaling Considerations

```
Current Scale:              Future Scale:
┌─────────────┐            ┌─────────────┐
│  1K Docs    │            │  1M+ Docs   │
│  Single DB  │────────────│ Distributed │
│  Local      │            │  Cloud DB   │
└─────────────┘            └─────────────┘
       │                          │
       │                          │
       ▼                          ▼
┌─────────────┐            ┌─────────────┐
│  Good for:  │            │  Good for:  │
│  • Personal │            │  • Enterprise
│  • Small    │            │  • Production
│    team     │            │  • High load│
│  • Testing  │            │  • Multi-user
└─────────────┘            └─────────────┘
```

---

**These diagrams illustrate the architecture and data flows of your RAG agent system!**
