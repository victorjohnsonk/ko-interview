# Modo Energy — Ko (AI Analyst) Take-Home

## Task Overview

Your task is to build an MCP (Model Context Protocol) server that wraps the **Modo Energy public API**, allowing an LLM to query battery energy storage data through natural conversation.

Your server should expose 2–4 tools and be installable into Claude Code (or a similar MCP client).

Please spend **no more than 2 hours** on this task.

You are encouraged to use AI coding tools (Claude Code, Cursor, Copilot, etc). Please include a short note in your README stating which AI tools and models you had available.

## Development Considerations

I began by understanding the Modo Energy API endpoints and their capabilities. To move quickly, I first mocked a very simple endpoint and built a minimal MCP tool around it. This helped validate the overall structure and interaction pattern early on.
 
From there, I implemented MCP tools with clear and concise docstrings so they are easily interpretable by an LLM. While exploring the API, I identified that the `/indices/{id}/` endpoint was not available as expected, so it was removed from the design to avoid unnecessary complexity and broken calls.
 
Initially, the tools were implemented without strict input/output validation to prioritise rapid iteration and ensure useful responses. Validation was later partially introduced based on the API documentation (e.g. typed `Literal`s for enums such as `market_region`, `granularity`, etc.) to improve correctness while maintaining flexibility.
 
### API Client & Request Handling
 
A lightweight HTTP client was implemented using the Python standard library (`urllib`) to avoid external dependencies and keep the solution portable. This includes:
 
- A centralised request builder with consistent query parameter handling  
- Automatic cleaning of parameters (e.g. removing `None`, encoding booleans, handling repeated query params like `markets`)  
- Structured error handling via a custom `ModoAPIError`, including surfaced HTTP status codes and response payloads  
- Configurable base URL, timeout, and user agent via environment variables  
 
### Pagination Strategy
 
Cursor-based pagination is handled explicitly and abstracted away from the MCP tools:
 
- A helper (`extract_cursor`) supports multiple cursor formats (`next_cursor`, `cursor`, or cursor embedded in `next` URLs`)  
- “Fetch-all” helper functions aggregate paginated results into a single response  
- A `max_pages` safeguard prevents unbounded requests  
 
This keeps the MCP tools simple while still supporting full dataset retrieval when needed.
 
### Project Structure
 
The codebase is structured with clear separation of concerns:
 
- `client.py` — HTTP layer and error handling  
- `services.py` — API interaction and business logic  
- `tools.py` — MCP tool definitions and schemas  
- `config.py` — environment-based configuration  
 
This modular approach makes it easy to extend functionality (e.g. adding new endpoints or tools) without affecting existing components.
 
### Transport & Testing
 
For testing, I initially used HTTP as the MCP transport method for ease of debugging. During this phase, I exposed the local server via ngrok and connected it directly to ChatGPT as a custom MCP endpoint. This allowed me to test the tools in a realistic conversational workflow. I had a similar setup from a previous MCP project, so this integration was quick to configure.
 
After validation, I switched to `stdio` transport to align with typical MCP client environments such as Claude Code.
 
### Trade-offs & Time Constraints
 
Given the 2-hour time constraint, I prioritised:
 
- Working end-to-end functionality over full validation coverage  
- Clean abstractions over exhaustive edge-case handling  
- Minimal dependencies for faster setup and portability  
 
Some areas (e.g. stricter schema validation, retries, and richer error mapping) were intentionally left as future improvements.
 
### Use of AI Tools
 
To accelerate development, I used ChatGPT (GPT-5.3, Pro Subscription) for:

- Generating input/output validation schemas from API documentation  
- Writing and refining MCP tool docstrings  
- Creating example test queries  
- Test MCP endpoint (exposed visa ngroka and transport set to http)
- Enhancing and refining this README for clarity and structure  
 
Overall, the task was completed in under two hours, with a focus on clarity, extensibility, and pragmatic engineering trade-offs.

| Category | Example Queries |
|----------|----------------|
| **Discovery** | What indices are available in Great Britain?<br>Show me all non-custom indices in ERCOT.<br>Which battery indices exist in CAISO?<br>List all indices across all regions.<br>What indices can I analyse in NEM? |
| **Index Inspection** | What does the GB battery index include?<br>How is the ERCOT battery index defined?<br>What assets are included in this index?<br>Give me details of the CAISO battery index.<br>What filters are used in this index? |
| **Aggregated Revenue** | What was total revenue for the GB battery index last year?<br>Compare total revenues across all indices in 2025.<br>How much revenue did this index generate in Q1 2024?<br>Break down revenue by market for this index in 2024.<br>Which markets contributed most to revenue in 2025? |
| **Revenue Timeseries** | How has revenue evolved over time for the GB battery index?<br>Show weekly revenue trends for ERCOT batteries.<br>What are the daily revenues for this index in January 2025?<br>Plot monthly revenue trends for 2024.<br>How volatile is revenue over time? |
| **Full Dataset / Pagination** | Give me the full revenue history for this index.<br>Download all revenue data for 2023–2025.<br>Analyse long-term revenue trends since 2022.<br>Show the complete monthly revenue history.<br>Compare yearly trends across multiple years. |
| **Capacity Timeseries** | How has battery capacity grown in ERCOT over the past year?<br>What is the capacity trend for GB battery assets?<br>Show installed capacity over time for this index.<br>How much capacity was added in 2024?<br>Compare capacity growth across regions. |
| **Advanced Analytics** | Which index performed the best in 2024?<br>Compare monthly revenues in Q1 2025.<br>How has battery capacity growth in ERCOT impacted revenues?<br>Which index generated the most revenue and from which markets?<br>Analyse revenue and capacity trends for GB batteries over the last 2 years.<br>Which index has the most volatile revenue profile?<br>Which index generates the most revenue per MW? |

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
| `GET /indices/{id}/` | Get details of a single index, including its definition (asset filters, region, etc). THIS ENDPOINT RETURNED 404 AND IS EXCLUDED FROM TOOLS. |
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


