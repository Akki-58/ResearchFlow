from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatMistralAI(model = "ministral-8b-latest", temperature=0, api_key=os.getenv("MISTRAL_API_KEY"))

# 4 agents
# 1. Search Agent using create_agent() from langchain.agents - just pass the model and tools (web_search tool) and it returns a ready-to-use agent graph powered by LangGraph internally (no AgentExecutor or hub prompts needed)
# 2. Reader Agent using the same pattern but with the scrape_url tool
# 3. Writer Chain using the modern LCEL pipe (runables) syntax - prompt | llm | StrOutputParser() which takes all the research and writes a full report.
# 4. Critic Chain again using LCEL pipe which reads the report and gives a score and feedback.

# Search Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools= [web_search]
    )

# Reader Agent
def build_reader_agent():
    return create_agent(
        model= llm,
        tools= [scrape_url]
    )

# Writer Chain
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert research writer.

Write clear, structured, factual and insightful research reports.

When critic feedback is provided, revise the report accordingly.
Do not blindly accept the critic's suggestions if they contradict
the supplied research evidence."""
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research_combined}

Previous Report:
{previous_report}

Critic Feedback:
{feedback}

Instructions:

1. If there is no Previous Report, create the report from scratch.
2. If a Previous Report exists, revise it based on the Critic Feedback.
3. Only make factual claims supported by the research.
4. Remove unsupported claims.
5. Fix missing information identified by the critic.
6. Improve clarity, structure and factual accuracy.
7. Preserve useful information from the previous report.

Structure the report as:

- Introduction
- Key Findings
  - Minimum 3 well-explained points
- Important Statistics and Data
- Expert Perspectives
- Challenges and Risks
- Emerging Trends and Future Outlook
- Conclusion
- Sources

For Sources, list all URLs found in the research.

Be detailed, factual and professional.

Return ONLY the final research report."""
    ),
])
# writer_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
#     ("human", """Write a detailed research report on the topic below.

# Topic: {topic}

# Research Gathered:
# {research}

# Structure the report as:
# - Introduction
# - Key Findings (minimum 3 well-explained points)
# - Important Statistics and Data
# - Expert Perspectives
# - Challenges and Risks
# - Emerging Trends and Future Outlook
# - Conclusion
# - Sources (list all URLs found in the research)

# Be detailed, factual and professional."""),
# ])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic chain
CRITIC_PROMPT = """
Review the research report below rigorously.

Topic:
{topic}

Research:
{research}

Report:
{report}

Check:

- Accuracy
- Missing information
- Unsupported claims
- Contradictions with the research
- Source quality
- Structure
- Important statistics and data
- Expert perspectives
- Challenges and risks
- Emerging trends
- Whether the conclusion follows from the evidence

Return EXACTLY this format:

SCORE: X/10

ISSUES:
- issue 1
- issue 2
- issue 3

IMPROVEMENTS:
- improvement 1
- improvement 2
- improvement 3

FINAL VERDICT:
PASS

or:

FINAL VERDICT:
REVISE

Only return PASS if:

- Evidence is strong
- There are no major unsupported claims
- There are no important factual problems
- Coverage is sufficiently comprehensive
- The report is well structured
"""


critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp and constructive research critic. "
        "Be honest, specific and evidence-based."
    ),
    (
        "human",
        CRITIC_PROMPT
    ),
])
# CRITIC_PROMPT = """
# Review below report rigorously.
# Report: {report}

# Check:
# - Accuracy
# - Missing information
# - Unsupported claims
# - Structure

# Return:

# SCORE: X/10

# ISSUES:
# - ...

# IMPROVEMENTS:
# - ...

# FINAL VERDICT:
# PASS or REVISE
# Only return PASS if:
# - Evidence is strong
# - No major unsupported claims exist
# - Coverage is comprehensive
# """
# critic_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
#     ("human", CRITIC_PROMPT),
# ])

critic_chain = critic_prompt | llm | StrOutputParser()
