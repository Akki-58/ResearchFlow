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
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Important Statistics and Data
- Expert Perspectives
- Challenges and Risks
- Emerging Trends and Future Outlook
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic chain
CRITIC_PROMPT = """
Review below report rigorously.
Report: {report}

Check:
- Accuracy
- Missing information
- Unsupported claims
- Structure

Return:

SCORE: X/10

ISSUES:
- ...

IMPROVEMENTS:
- ...

FINAL VERDICT:
PASS or REVISE
Only return PASS if:
- Evidence is strong
- No major unsupported claims exist
- Coverage is comprehensive
"""
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", CRITIC_PROMPT),
])

critic_chain = critic_prompt | llm | StrOutputParser()
