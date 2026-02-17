from __future__ import annotations

import urllib.parse
import xml.etree.ElementTree as ET

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("arxiv-tools")


@mcp.tool()
async def arxiv_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Search arXiv (free public API).
    query example: "RAG evaluation"
    """
    q = query.strip()
    if not q:
        return []

    max_results = max(1, min(int(max_results), 10))
    encoded = urllib.parse.quote(q)

    url = (
        "http://export.arxiv.org/api/query"
        f"?search_query=all:{encoded}&start=0&max_results={max_results}"
    )

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, headers={"User-Agent": "mcp-arxiv-tool/1.0"})
        r.raise_for_status()
        xml_text = r.text

    root = ET.fromstring(xml_text)

    # arXiv Atom uses namespaces
    ns = {"a": "http://www.w3.org/2005/Atom"}

    out: list[dict] = []
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip()
        summary = (entry.findtext("a:summary", default="", namespaces=ns) or "").strip()
        link = ""
        for l in entry.findall("a:link", ns):
            if l.attrib.get("rel") == "alternate":
                link = l.attrib.get("href", "")
                break

        out.append(
            {
                "title": title,
                "summary": summary[:800],  # keep it short
                "url": link,
            }
        )

    return out


if __name__ == "__main__":
    mcp.run()
