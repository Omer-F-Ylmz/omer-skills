"""Hermes mcp-serve stdio sınaması: initialize + tools/list + bir araç çağrısı (araclar/hermes venv'iyle koş)."""
import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

KOK = Path(__file__).resolve().parents[1]
PARAMS = StdioServerParameters(
    command=str(KOK / "araclar/hermes/Scripts/hermes.exe"),
    args=["mcp-serve"],
    env={**os.environ, "HERMES_HOME": str(KOK / "araclar/hermes-home"), "PYTHONUTF8": "1"},
)


async def main() -> int:
    async with stdio_client(PARAMS) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            araclar = [t.name for t in (await s.list_tools()).tools]
            print("tools:", ",".join(araclar))
            if "conversations_list" in araclar:
                sonuc = await s.call_tool("conversations_list", {})
                print("conversations_list isError:", sonuc.is_error)
            return 0 if araclar else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(asyncio.wait_for(main(), 60)))
