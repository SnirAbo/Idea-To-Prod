import asyncio
import os
from dotenv import load_dotenv
from agno.agent import Agent
from config.models import CODE_GEN_MODEL
from mcp_servers import get_github_tools , get_jira_tools
from config.settings import JIRA_PROJECT_KEY
from agno.tools.shell import ShellTools

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
        "CRITICAL: generate EVERY file the code imports or references. If "
        "any file imports './components/Editor' or '@/utils/foo', that file "
        "MUST also be created with real, working content — never leave an "
        "import pointing to a file you did not create. "
        "Then, using your GitHub tools, create a new GitHub repository and "
        "push all the generated files to it as the initial commit. "
        "\n\n"
        "SELF-CHECK (verify the code actually works before finishing):\n"
        "After pushing, use your Shell tools to clone the repository you "
        "just created into a local folder, then run the install command "
        "(detect the package manager from the lock file / package.json; use "
        "'npm install --legacy-peer-deps' for npm projects to tolerate peer "
        "conflicts) and then the build command (e.g. 'npm run build'). "
        "If install or build FAILS, read the error, fix the offending files "
        "(wrong/non-existent dependency versions, missing source files, "
        "ESM/CommonJS config mismatches, broken imports), and push the fixes "
        "to the same repository. Then clone fresh and run install + build "
        "again to confirm. "
        "Repeat this fix-and-verify cycle AT MOST 3 times. If build still "
        "fails after 3 attempts, push whatever you have and continue — do "
        "not loop forever. "
        "You are on Windows (PowerShell); chain shell commands with ';', not "
        "'&&'. "
        "\n\n"
        "After the code builds (or after 3 attempts), mark each task as Done "
        "in Jira. Do this SEQUENTIALLY — one issue at a time, not in "
        "parallel — and for each issue first get its available transitions, "
        "then apply the Done transition, before moving to the next issue. "
        "Finally, return the URL of the new GitHub repository you created."
    ),
    tools=[jira_tools, github_tools, ShellTools()],
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