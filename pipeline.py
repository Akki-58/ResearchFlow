from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# base function
def run_research_pipeline(topic: str) -> dict:

    state = {}

    # search agent working
    print("\n"+ "-"*50)
    print("Step 1: Search Agent is Working")
    print("-"*50+'\n')

    search_agent = build_search_agent()
#     SEARCH_PROMPT = f"""You are a professional research search agent.

# Research Topic: {topic}

# Your task:

# 1. Find 10-15 high-quality sources.
# 2. Prioritize:
#    - Official documentation
#    - Academic papers
#    - Government websites
#    - Industry reports
#    - Reputable news sources

# 3. For each source provide:

# SOURCE N
# Title:
# URL:
# Source Type:
# Publication Date:

# 4. After listing sources, provide:

# ## Key Findings
# - Bullet point findings extracted from multiple sources.

# ## Research Gaps
# - Missing areas that require deeper reading.

# Rules:
# - Prefer information from the last 12 months.
# - Avoid low-quality blogs.
# - Do not summarize before listing sources.
# - Always include URLs.
# """
    SEARCH_PROMPT = f"""You are a professional research search agent. Find the best sources for: {topic}

Return EXACTLY:

URLS:
1. <url>
2. <url>
3. <url>
...

Then:

SUMMARY:
- key finding
- key finding
- key finding
...

Rules:
- Return 20 high-quality URLs.
- Prioritize official docs, research papers, government sites, reputable publications.
- Put URLs at the top.
- No long explanations.
"""
    search_result = search_agent.invoke({
        "messages": [("user", SEARCH_PROMPT)]
    })
    state["search_results"] = search_result["messages"][-1].content

    print("\n search result : ", state['search_results'])

    # reader agent
    print("\n"+ "-"*50)
    print("Step 2: Reader Agent is scrapping top resources...")
    print("-"*50+'\n')

    reader_agent = build_reader_agent()
    READER_PROMPT = f"""You are a research reader agent.

Topic:{topic}

Search Results: {state['search_results'][:1000]}

Tasks:
1. Identify all URLs present in the Search Results.

2. Rank URLs by:
   - Relevance to the topic
   - Authority of the source
   - Likelihood of successful scraping

3. Select and scrape at least 3 URLs.
   - If more relevant URLs are available, scrape up to 5.
   - Do NOT stop after scraping a single URL.
   - Skip URLs that cannot be accessed or scraped.

Output Format:

SELECTED URL: <url>

DETAILED EXTRACTION: Include if present : Executive Summary, Key Facts, Statistics, Expert Insights, Recent Developments, Limitations

Only use information directly found in the source.
Do not invent information.
"""
    reader_result = reader_agent.invoke({
        "messages": [("user", READER_PROMPT)]
    })
    state['scrapped_content'] = reader_result['messages'][-1].content
    print("\nScrapped Content: \n", state['scrapped_content'])

    # writer chain
    print("\n"+ "-"*50)
    print("Step 3: Writer is drafting a report...")
    print("-"*50)

    research_combined = (
        f"SEARCH RESULTS: \n {state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT: \n {state['scrapped_content']}"
    )

    state['report'] = writer_chain.invoke({
        "topic" : topic,
        "research": research_combined
    })

    print("\n Final Report\n", state['report'])

    # critic chain
    print("\n"+ "-"*50)
    print("Step 4: Critic is reviewing the report...")
    print("-"*50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\n critic report \n", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\nEnter a research topic: ") 
    run_research_pipeline(topic = topic)