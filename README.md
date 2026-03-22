# Modo Energy — Ko (AI Analyst) Take-Home

## Task Overview

Your task is to build an MCP (Model Context Protocol) server that wraps the **Modo Energy public API**, allowing an LLM to query battery energy storage data through natural conversation.

Your server should expose 2–4 tools and be installable into Claude Code (or a similar MCP client).

Please spend **no more than 2 hours** on this task.

You are encouraged to use AI coding tools (Claude Code, Cursor, Copilot, etc). Please include a short note in your README stating which AI tools and models you had available.

## Background: Modo Indices

Modo Energy tracks the performance of battery energy storage systems (BESS) across multiple markets. A **Modo Index** represents a benchmark portfolio of battery assets in a given region. Think of it like a stock market index, but for batteries.

Each index tracks:
- **Revenue** — how much money the batteries in the index earned, broken down by market (e.g. wholesale trading, balancing mechanism, capacity market, ancillary services)
- **Capacity** — the total MW (power) and MWh (energy) of assets in the index over time

Indices exist for multiple regions: **GB**, **ERCOT** (Texas), **NEM** (Australia), and **CAISO** (California).

Revenue can be normalised (per MW or per MWh) and expressed over different time bases (per hour, per year) to allow fair comparison across assets of different sizes and across different time periods.

## The API

- **Getting started:** https://developers.modoenergy.com/docs/getting-started
- **Indices API reference:** https://developers.modoenergy.com/reference/index-list

Base URL: `https://api.modoenergy.com/pub/v1`

The following **Indices** endpoints are free to use, i.e. no API key or authentication required:

| Endpoint | Description |
|----------|-------------|
| `GET /indices/` | List all available indices. Filter by `market_region` (gb, ercot, nem, caiso) and `is_custom` (true/false). |
| `GET /indices/{id}/` | Get details of a single index, including its definition (asset filters, region, etc). |
| `GET /indices/{id}/revenue/` | Aggregated revenue for an index over a date range. Supports `capacity_normalisation` (mw, mwh), `time_basis` (hour, year), `breakdown` (market), and `markets` filtering. |
| `GET /indices/{id}/revenue/timeseries/` | Revenue as a time series. Adds `granularity` (base, daily, weekly, monthly). Cursor-paginated. |
| `GET /indices/{id}/capacity/timeseries/` | MW and MWh capacity over time. Filter by `date_from` / `date_to`. Cursor-paginated. |

## Getting started

### Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# or with Homebrew
brew install uv
```

### Set up the project


```bash
# Clone this repo
git clone https://github.com/victorjohnsonk/ko-interview.git
cd ko-interview

# Create a virtual environment and install dependencies
uv sync

# Run the server directly
uv run main.py
```

### Install into an MCP client

**Claude Code:**

```bash
claude mcp add modo-mcp -- uv run main.py
```

**Cursor:** Add to your `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "modo-mcp": {
      "command": "uv",
      "args": ["run", "main.py"],
      "cwd": "/path/to/ko-interview"
    }
  }
}
```

Then start your MCP client and verify the hello world tool works.


