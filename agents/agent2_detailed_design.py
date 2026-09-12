import asyncio
import sys


from dotenv import load_dotenv
from agno.agent import Agent
from config.models import DETAILED_DESIGN_MODEL
from mcp_servers import get_drive_tools , get_jira_tools
from agents.agent1_hl_design import run_agent1  


load_dotenv()  # Load environment variables from .env file

drive_tools = get_drive_tools();
jira_tools = get_jira_tools();

agent = Agent(
    name="Detailed Design Agent",
    model=DETAILED_DESIGN_MODEL,
    instructions=(
        "You are a software design assistant. You will be given a reference "
        "(link or file id) to a high-level design document stored in Google "
        "Drive. First, read the full content of that document using your "
        "Google Drive tools. "
        "Based on it, create a very detailed design document, broken down "
        "phase by phase — for each phase, describe the specific components, "
        "data models, APIs, and implementation details needed to build it. "
        "Then do the following two things: "
        "1) Save the detailed design as a new document in Google Drive, using "
        "your Google Drive tools. "
        "2) Extract concrete, actionable development tasks from the detailed "
        "design — one task per meaningful unit of work — and create each of "
        "them as a work item (issue) in Jira, using your Jira tools. Use the "
        "Jira project with key 'ITP' for all issues. Do not ask the user for "
        "confirmation, a project key, labels, or an assignee before creating "
        "the issues — proceed automatically using sensible defaults (issue "
        "type: Task). "
        "When tagging tasks by area (backend, frontend, infra, etc.), use "
        "Jira labels, not components — this Jira project has no pre-defined "
        "components, and Jira rejects issues that reference a component "
        "that doesn't already exist in the project. "
        "Return both the link to the saved detailed design document and a "
        "short summary of the Jira tasks you created."
    ),
    tools=[drive_tools, jira_tools],
    markdown=True,
    debug_mode=True,
)

async def run_agent2(hl_design_ref: str) -> str:
    async with drive_tools, jira_tools:
        response = await agent.arun(f"High-level design reference: {hl_design_ref}")
        return response.content

if __name__ == "__main__":

    idea = sys.argv[1] if len(sys.argv) > 1 else input("Enter an app idea: ")

    async def main():
        hl_design_ref = await run_agent1(idea)
        return await run_agent2(hl_design_ref)

    result = asyncio.run(main())
    print(result)