from __future__ import annotations

from duckduckgo_search import DDGS
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("search-tools")


@mcp.tool()
def ddg_search(query: str, max_results: int = 5) -> list[dict]:
    """
    DuckDuckGo text search (free). Returns a small list of results.
    """
    q = query.strip()
    if not q:
        return []

    max_results = max(1, min(int(max_results), 10))

    results: list[dict] = []
    with DDGS() as ddgs:
        for item in ddgs.text(q, max_results=max_results):
            results.append(
                {
                    "title": item.get("title"),
                    "url": item.get("href"),
                    "snippet": item.get("body"),
                }
            )
    return results


if __name__ == "__main__":
    mcp.run()
