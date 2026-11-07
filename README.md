# Idea-To-Prod

An MCP server that turns a natural-language application idea into a tested,
deployed codebase through a multi-agent pipeline.

Built with [FastMCP](https://github.com/jlowin/fastmcp) and the
[Agno](https://github.com/agno-agi/agno) agent framework, it exposes a single
MCP tool — `ideaToProd(idea: str)` — that orchestrates five specialized agents,
each responsible for one stage of the software delivery lifecycle.

## How it works

`ideaToProd("a quiz app with a timer")` runs the idea end-to-end:

| # | Agent | Responsibility | Output | Model |
|---|-------|----------------|--------|-------|
| 1 | HL Design | High-level design document | Google Drive | `gpt-5-mini` |
| 2 | Detailed Design | Phase-by-phase design + dev tasks | Google Drive + Jira | `gpt-5-mini` |
| 3 | Code Generation | Full application code | New GitHub repo | `gpt-5` |
| 4 | Unit Tests | Generates unit tests (different model than code-gen) | Same GitHub repo | `claude-sonnet-5` |
| 5 | Test Execution | Runs the tests; loops back to Agent 4 on failure | Pass/fail verdict | `claude-haiku-4-5` |

> Agent 6 (deployment) is scaffolded as an optional future stage.

The agents are chained in `orchestrator.py`; `server.py` wraps the pipeline as
an MCP tool so it can be driven from any MCP client.

## Architecture 
server.py # FastMCP server — exposes the ideaToProd tool
orchestrator.py # Chains agents 1→5, extracts the generated repo URL
mcp_servers.py # Factory functions for the Google Drive / Jira / GitHub MCP toolkits
config/
models.py # Which model each agent uses
settings.py # JIRA_PROJECT_KEY and other settings
agents/
agent1_hl_design.py
agent2_detailed_design.py
agent3_code_gen.py
agent4_unit_tests.py
agent5_test_execution.py


## Prerequisites

- **Python 3.13**
- **Docker** — runs the official GitHub MCP server (`ghcr.io/github/github-mcp-server`)
- **Node.js / npx** — runs the Google Drive MCP server
- **`mcp-atlassian`** — the Jira MCP server (installed via `uvx` or `pip`)
- **Playwright** — used by Agent 5 to execute tests

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root (it is gitignored):
   ```env
   OPENAI_API_KEY=your_openai_key
   ANTHROPIC_API_KEY=your_anthropic_key
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_USERNAME=your_email
   JIRA_API_TOKEN=your_jira_token
   GITHUB_PERSONAL_ACCESS_TOKEN=your_github_pat   # needs 'repo' + 'workflow' scopes
   ```
3. Complete the Google Drive OAuth flow once (handled by the Google Drive MCP server).
```
npx -y @piotr-agier/google-drive-mcp auth
```
4. Make sure Docker Desktop is running before starting the pipeline.
   you can also check if it works manualy before letting the agents use it
   with this command :
   ```
   docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN="docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token  ghcr.io/github/github-mcp-server"  ghcr.io/github/github-mcp-server
   ```

## Usage

**As an MCP server** (for use from an MCP client):
```bash
python server.py
```
The client then calls the `ideaToProd` tool with an idea string.

**Directly** (for local testing):
```bash
python -m orchestrator
```
You'll be prompted to enter an idea, and the pipeline runs end-to-end in the terminal.

## Notes

- Each MCP toolkit is created fresh per use (factory pattern in `mcp_servers.py`)
  to avoid anyio cancel-scope issues when reusing connections across tasks.
- `.env`, `mcp.json`, and `debug_output.txt` are gitignored and never committed.

