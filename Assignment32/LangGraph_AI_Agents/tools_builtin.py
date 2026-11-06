"""PART 1 - Task 2: built-in LangChain tools (Wikipedia, web search, arXiv).

Run:  python tools_builtin.py        (needs internet, no LLM / API key)

Steps required by the assignment: 1) initialise the tools  2) test each one  3) print outputs.
"""
import os

from langchain_community.tools import ArxivQueryRun, DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper


# ---------------------------------------------------------------- Step 1: initialise
def get_wikipedia_tool():
    """Wikipedia lookup (returns short page summaries)."""
    return WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=800))


def get_web_search_tool():
    """Web search. Uses Tavily when TAVILY_API_KEY is set, otherwise free DuckDuckGo (no key)."""
    if os.getenv("TAVILY_API_KEY"):
        from langchain_tavily import TavilySearch
        return TavilySearch(max_results=3)
    return DuckDuckGoSearchRun()


def get_arxiv_tool():
    """arXiv research-paper search."""
    return ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=600))


def get_builtin_tools():
    """All built-in tools that can be initialised (a missing optional package is skipped with a warning)."""
    tools = []
    for factory in (get_wikipedia_tool, get_web_search_tool, get_arxiv_tool):
        try:
            tools.append(factory())
        except Exception as e:
            print(f"[warning] {factory.__name__} unavailable: {e}")
    return tools


# ---------------------------------------------------------------- Steps 2 & 3: test + print
if __name__ == "__main__":
    tests = [
        ("Wikipedia", get_wikipedia_tool, "Alan Turing"),
        ("Web search", get_web_search_tool, "latest LangChain release"),
        ("arXiv", get_arxiv_tool, "ReAct: Synergizing Reasoning and Acting in Language Models"),
    ]
    for label, factory, query in tests:
        print(f"\n===== {label} tool =====")
        try:
            tool = factory()                                   # Step 1: initialise
            print("Name       :", tool.name)
            print("Description:", tool.description[:110], "...")
            print("Query      :", query)
            print("Output     :", str(tool.invoke(query))[:500])     # Steps 2 & 3: test + print
        except Exception as e:                                 # no internet, missing package, rate limit ...
            print("Tool failed:", e)
