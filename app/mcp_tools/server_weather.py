from __future__ import annotations

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-tools")


@mcp.tool()
async def current_weather(latitude: float, longitude: float) -> dict:
    """
    Get current weather from Open-Meteo (free, no API key).
    """
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current_weather=true"
    )

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers={"User-Agent": "mcp-weather-tool/1.0"})
        if r.status_code != 200:
            return {"ok": False, "error": f"Open-Meteo error: {r.status_code}"}
        data = r.json()

    cw = data.get("current_weather") or {}
    return {
        "ok": True,
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "temperature": cw.get("temperature"),
        "windspeed": cw.get("windspeed"),
        "winddirection": cw.get("winddirection"),
        "time": cw.get("time"),
    }


if __name__ == "__main__":
    mcp.run()
