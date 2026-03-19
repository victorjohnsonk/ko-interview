"""
Modo Energy MCP Server

An MCP server that exposes the Modo Energy public API — specifically the
Indices endpoints — as tools that can be called by LLMs via Claude Code
or any MCP-compatible client.

See README.md for the full task brief.
"""

from fastmcp import FastMCP

mcp = FastMCP("Modo Energy")

BASE_URL = "https://api.modoenergy.com/pub/v1"


@mcp.tool
def hello() -> str:
    """Say hello — replace this with your own tools."""
    return "Hello from Modo Energy! Good luck on the assessment!"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
