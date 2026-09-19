from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

from metrics import ResearchMetrics


# base function
def run_research_pipeline(topic: str,
    max_revisions: int = 2) -> dict:

    state = {}

    metrics = ResearchMetrics()
    metrics.start()

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

    metrics.count_search_sources(
        state["search_results"]
    )

    print("\n search result : ", state['search_results'])

    # reader agent
    print("\n"+ "-"*50)
    print("Step 2: Reader Agent is scrapping top resources...")
    print("-"*50+'\n')

    reader_agent = build_reader_agent()
    READER_PROMPT = f"""You are a research reader agent.

Topic:{topic}

Search Results: {state['search_results']}

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

    metrics.count_scraped_sources(
        state["scrapped_content"]
    )

    print("\nScrapped Content: \n", state['scrapped_content'])

    # writer chain
    print("\n"+ "-"*50)
    print("Step 3: Writer is drafting a report...")
    print("-"*50)

    research_combined = (
        f"SEARCH RESULTS: \n {state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT: \n {state['scrapped_content']}"
    )

    # Writer + Critic Revision Loop
    print("\n" + "-" * 50)
    print("Step 3: Writer + Critic Revision Loop")
    print("-" * 50)

    MAX_REVISIONS = max_revisions

    previous_report = ""
    feedback = ""

    for iteration in range(MAX_REVISIONS + 1):

        print(
            f"\n--- Writing iteration "
            f"{iteration + 1}/{MAX_REVISIONS + 1} ---"
        )

        # ----------------------------------------------
        # Writer
        # ----------------------------------------------

        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research_combined": research_combined,
            "previous_report": previous_report,
            "feedback": feedback
        })

        print("\nReport generated.")

        # ----------------------------------------------
        # Critic
        # ----------------------------------------------

        print("\nCritic is reviewing the report...")

        state["feedback"] = critic_chain.invoke({
            "topic": topic,
            "research": research_combined,
            "report": state["report"]
        })

        metrics.add_iteration(
            iteration_number=iteration + 1,
            report=state["report"],
            feedback=state["feedback"]
        )

        print("\nCritic feedback:\n")
        print(state["feedback"])

        # ----------------------------------------------
        # Check verdict
        # ----------------------------------------------

        critic_output = state["feedback"].upper()

        if "FINAL VERDICT:" in critic_output:

            verdict_section = critic_output.split(
                "FINAL VERDICT:",
                1
            )[1].strip()

            # Only inspect the first line after FINAL VERDICT
            verdict = verdict_section.splitlines()[0].strip()

        else:
            verdict = ""

        print(f"\nVerdict: {verdict}")

        # ----------------------------------------------
        # PASS
        # ----------------------------------------------

        if verdict == "PASS":
            print("\n" + "-" * 50)
            print("RESEARCH PASSED CRITIC REVIEW")
            print("-" * 50)

            state["revision_count"] = iteration

            break

        # ----------------------------------------------
        # Maximum revisions reached
        # ----------------------------------------------

        if iteration >= MAX_REVISIONS:
            print("\n" + "-" * 50)
            print("MAXIMUM REVISIONS REACHED")
            print("-" * 50)

            state["revision_count"] = iteration
            break

        # ----------------------------------------------
        # Prepare next revision
        # ----------------------------------------------

        previous_report = state["report"]
        feedback = state["feedback"]

        print("\nCritic requested revision.")
        print("Sending feedback back to writer...")

    # state['report'] = writer_chain.invoke({
    #     "topic" : topic,
    #     "research": research_combined
    # })

    # print("\n Final Report\n", state['report'])

    # # critic chain
    # print("\n"+ "-"*50)
    # print("Step 4: Critic is reviewing the report...")
    # print("-"*50)

    # state["feedback"] = critic_chain.invoke({
    #     "report": state["report"]
    # })

    # print("\n critic report \n", state['feedback'])

    metrics.calculate_report_metrics(
        state["report"]
    )

    metrics.stop()

    state["metrics"] = metrics.calculate()

    metrics.print_metrics()

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ") 
    run_research_pipeline(topic = topic)
    # to save responses