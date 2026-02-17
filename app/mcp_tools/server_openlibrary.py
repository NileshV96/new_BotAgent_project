from __future__ import annotations

import urllib.parse
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("openlibrary-tools")


@mcp.tool()
async def book_search(title: str, limit: int = 5) -> list[dict]:
    """
    Search books using OpenLibrary (free public API).
    """
    t = title.strip()
    if not t:
        return []

    limit = max(1, min(int(limit), 10))
    encoded = urllib.parse.quote(t)
    url = f"https://openlibrary.org/search.json?title={encoded}&limit={limit}"

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers={"User-Agent": "mcp-openlibrary-tool/1.0"})
        r.raise_for_status()
        data = r.json()

    docs = data.get("docs") or []
    out: list[dict] = []
    for d in docs[:limit]:
        key = d.get("key")  # e.g. "/works/OL123W"
        out.append(
            {
                "title": d.get("title"),
                "author": (d.get("author_name") or [None])[0],
                "first_publish_year": d.get("first_publish_year"),
                "openlibrary_url": f"https://openlibrary.org{key}" if key else None,
            }
        )
    return out


if __name__ == "__main__":
    mcp.run()
