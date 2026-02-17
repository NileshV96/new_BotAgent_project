from __future__ import annotations

import urllib.parse
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("wiki-tools")


@mcp.tool()
async def wiki_summary(title: str) -> dict:
    """
    Get a short Wikipedia summary for a page title.
    Example: title="LangChain"
    """
    safe = urllib.parse.quote(title.strip().replace(" ", "_"))
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{safe}"

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers={"User-Agent": "mcp-wiki-tool/1.0"})
        if r.status_code != 200:
            return {
                "ok": False,
                "title": title,
                "error": f"Wikipedia API error: {r.status_code}",
                "hint": "Try a simpler title (e.g., 'Mumbai' instead of long sentence).",
            }

        data = r.json()

    return {
        "ok": True,
        "title": data.get("title", title),
        "extract": data.get("extract"),
        "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
    }


if __name__ == "__main__":
    mcp.run()
