import asyncio
import os
from dotenv import load_dotenv
from agno.agent import Agent
from config.models import CODE_GEN_MODEL
from mcp_servers import get_github_tools , get_jira_tools
from config.settings import JIRA_PROJECT_KEY

load_dotenv()  

jira_tools = get_jira_tools();
github_tools = get_github_tools();

agent = Agent(
    name="Code Generation Agent",
    model=CODE_GEN_MODEL,
    instructions=(
        "You are a software engineer assistant that turns Jira work items "
        "into a complete, working codebase. "
        "You will be given a Jira space key (also referred to as a project "
        "key by the underlying Jira tools) — use it to pull all the open "
        "development tasks (work items) from that space using your Jira "
        "tools. Read the tasks ONCE using a single search call; do not "
        "call additional Jira tools per-issue. "
        "Based on those tasks, generate the full application code needed to "
        "implement every one of them — organized into a clean, runnable "
        "project structure with all necessary files (source code, "
        "configuration, a dependency manifest, and a README that explains "
        "how to run the project). "
        "Then, using your GitHub tools, create a new GitHub repository and "
        "push all the generated files to it as the initial commit. "
        "After the code is pushed, mark each task as Done in Jira. "
        "Do this SEQUENTIALLY — one issue at a time, not in parallel — and "
        "for each issue first get its available transitions, then apply the "
        "Done transition, before moving to the next issue. "
        "Finally, return the URL of the new GitHub repository you created."
    ),
    tools=[jira_tools, github_tools],
    markdown=True,
    debug_mode=True,
)

async def run_agent3() -> str:
    async with jira_tools, github_tools:
        response = await agent.arun(f"Jira project key: {JIRA_PROJECT_KEY}")
        return response.content



async def main():
    print("TOKEN:", os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "MISSING"))
    async with github_tools, jira_tools:
        await agent.aprint_response(
            f"Read all issues from Jira project '{JIRA_PROJECT_KEY}', "
            f"build the application they describe, create a new GitHub "
            f"repository, push all the code to it, and give me the repo URL."
        )


if __name__ == "__main__":
    asyncio.run(main())