# ResearchFlow

AI-powered multi-agent research automation system built using LangChain and Mistral AI.

ResearchFlow automates the end-to-end research workflow by combining specialized AI agents for:

- Web search and information retrieval
- Content extraction and reading
- Structured report generation
- Automated critique and evaluation
- Iterative report refinement

The project demonstrates modern agentic AI workflow design using modular AI agents and LangChain Expression Language (LCEL).

---

# Features

* Multi-agent architecture
* Automated web research pipeline
* Structured report generation
* AI-powered critique and evaluation
* Writer-Critic revision loop
* Modular tool integration
* LangChain LCEL pipelines
* Mistral AI integration
* Clean and extensible codebase

---

# Architecture

```text
                    ┌─────────────────────┐
                    │      User Query     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Search Agent      │
                    │  • Tavily Search    │
                    │  • 20 sources/query │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Reader Agent     │
                    │ • BeautifulSoup     │
                    │ • Extract relevant  │
                    │   information       │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │         Writer Agent            │
              │ • Synthesizes research          │
              │ • Generates structured report   │
              └────────────────┬───────────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │         Critic Agent            │
              │ • Checks quality                │
              │ • Finds gaps / unsupported info │
              └────────────────┬───────────────┘
                               │
                     Revision needed?
                        /             \
                      Yes              No
                       │                │
                       ▼                ▼
                ┌─────────────┐   ┌─────────────┐
                │   Writer    │   │ Final Report│
                │  Revision   │   └─────────────┘
                └──────┬──────┘
                       │
                       ▼
                   Critic
                 (2 cycles)
```

---

# Tech Stack

* Python
* LangChain
* Mistral AI
* LCEL (LangChain Expression Language)
* Prompt Engineering

---

# Project Structure

```bash
ResearchFlow/
│
├── agents.py        # AI agents and chains
├── tools.py         # Search/scraping tools
├── pipeline.py      # Workflow orchestration
├── requirements.txt
└── README.md
```

---

# Workflow

## 1. Search Agent

Searches the web for relevant information related to the user query.

## 2. Reader Agent

Processes and extracts useful information from retrieved content.

## 3. Writer Chain

Generates a structured research report containing:

* Introduction
* Key Findings
* Statistics
* Expert Perspectives
* Risks & Challenges
* Future Outlook
* Sources

## 4. Critic Chain

Evaluates:

* factual consistency
* unsupported claims
* report quality
* completeness

Provides feedback and scoring for the generated report.

## 5. Writer-Critic Revision Loop

ResearchFlow does not stop after the first generated draft.

The system performs two Writer-Critic revision cycles before producing the final report.

This creates a feedback-driven generation process rather than a single prompt-response workflow.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Akki-58/ResearchFlow.git
cd ResearchFlow
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_api_key_here
TAVILY__API_KEY=your_api_key_here
```

---

# Run the Project

```bash
python pipeline.py
```

---

# Example Use Case

### Input

```text
Impact of AI in Healthcare
```

### Output

* AI-generated research report
* insights and statistics
* source-backed analysis
* critique and evaluation summary

---

# Sample Pipeline Flow

```python
topic → search → read → synthesize → critique
```

---

# Key Concepts Demonstrated

* Agentic AI systems
* AI workflow orchestration
* Multi-agent collaboration
* Prompt engineering
* Automated research systems
* AI evaluation pipelines
* Modular LLM application design

---

# Why ResearchFlow?

Most simple AI applications rely on a single prompt-response workflow.

ResearchFlow instead separates responsibilities into specialized agents:

* retrieval
* reading
* synthesis
* critique

This improves modularity, scalability, and research quality.

---

# License

This project is open-source and available under the MIT License.
