import asyncio
from agno.agent import Agent
from agno.tools.shell import ShellTools
from dotenv import load_dotenv

from config.models import TEST_EXEC_MODEL

load_dotenv()  # Load environment variables from .env file

agent = Agent(
    name="Test Execution Agent",
    model=TEST_EXEC_MODEL,
    instructions=(
    "You are given a GitHub repository URL. Your job is to clone it, install "
    "its dependencies, run its tests ONCE, and report the result.\n\n"

    "WORKFLOW — follow this order strictly:\n"
    "1. Clone the repository with git into a local folder.\n"
    "2. Inspect the repo to find the stack and package manager (package.json + "
    "which lock file: pnpm-lock.yaml -> pnpm, yarn.lock -> yarn, "
    "package-lock.json -> npm). Also read the test script in package.json.\n"
    "3. INSTALL DEPENDENCIES FIRST — run the correct install command (e.g. "
    "'pnpm install' or 'npm install') and wait for it to finish. You CANNOT "
    "run tests before this; the test runner lives in the installed "
    "dependencies. If install fails, stop and report TESTS FAILED with the "
    "install error.\n"
    "4. Run the test command ONCE (the script defined in package.json).\n"
    "5. Report the result and STOP.\n\n"

    "HARD RULES:\n"
    "- Do NOT retry the test command over and over with different flags. Run "
    "install once, then tests once. If they fail, that is a valid result — "
    "report TESTS FAILED, do not keep trying new variations.\n"
    "- You are on Windows (PowerShell). In PowerShell use ';' to chain "
    "commands, NOT '&&'.\n"
    "- Only run commands needed to clone, install, and test — nothing else.\n"
    "- End your response with exactly one verdict line: 'TESTS PASSED' or "
    "'TESTS FAILED'."
    ),
    tools=[ShellTools()],
    markdown=True,
    debug_mode=True,
)

async def run_agent5(repo_url: str) -> str:
    response = await agent.arun(f"Run the tests for the GitHub repository {repo_url}")
    return response.content

async def main():
    await agent.aprint_response(
        "Run the tests for the GitHub repository "
        "https://github.com/SnirAbo/itp-habits-20260905"
    )


if __name__ == "__main__":
    asyncio.run(main())