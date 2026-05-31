from langchain.tools import tool
# to scrape
import requests
from bs4 import BeautifulSoup
# to make print function formatted
from rich import print

from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# tool 1 : Tavily for searching

# tool decorator (used to create tool)
@tool
def web_search(query : str) -> str:
    """Seach the web for recent and reliableinformation on a topic. Reterns Titles, URLs and snippets."""

    results = tavily.search(query=query, max_results=5)
    # to save tokens we take max_results

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )

    return "\n------\n".join(out)

# print(web_search.invoke("Learning LangChain and LangGraph"))

# tool 2 - BeautifulSoup Scrapping

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers = {"User-Agent": "Mozilla/5.0"})
        # resp will have whole raw html
        soup = BeautifulSoup(resp.text, "html.parser")
        # remove all the irrelevant tags
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
        # keeping 3000 so that api tokens are not fully utilized
    except Exception as e:
        return f"Couldn't scrape URL {url}: {str(e)}"

# print(scrape_url.invoke("https://xmcyber.com/blog/project-glasswing-mythos-findings"))
