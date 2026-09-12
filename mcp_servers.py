# mcp_servers.py
import os
from agno.tools.mcp import MCPTools


def get_drive_tools() -> MCPTools:
    """Build a NEW Google Drive MCP toolkit connection.

    A fresh instance is needed each time (rather than one shared object)
    because MCPTools ties its subprocess/task group to the async task that
    entered its `async with` block; reusing the same instance across
    separate `async with` blocks breaks anyio's cancel-scope tracking.
    """
    return MCPTools(command="npx -y @piotr-agier/google-drive-mcp")


def get_jira_tools() -> MCPTools:
    """Build a NEW Jira MCP toolkit connection (see get_drive_tools)."""
    env = os.environ.copy()
    env["JIRA_URL"] = os.environ.get("JIRA_URL", "")
    env["JIRA_USERNAME"] = os.environ.get("JIRA_USERNAME", "")
    env["JIRA_API_TOKEN"] = os.environ.get("JIRA_API_TOKEN", "")
    return MCPTools(command="mcp-atlassian", env=env)

def get_github_tools() -> MCPTools:
    """Build a NEW GitHub MCP toolkit connection (see get_drive_tools).

    Runs the official GitHub MCP server (github/github-mcp-server) via
    Docker. Requires Docker installed and GITHUB_PERSONAL_ACCESS_TOKEN
    set in the environment (docker run -e VAR with no value forwards
    the host env var through automatically).
    """
    token = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]
    return MCPTools(
        command=(
            f"docker run -i --rm "
            f"-e GITHUB_PERSONAL_ACCESS_TOKEN={token} "
            "ghcr.io/github/github-mcp-server"
        )
    )