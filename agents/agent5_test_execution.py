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
        "You are given a GitHub repository URL. Clone it locally, install its "
        "dependencies, run its tests, and report whether they passed.\n"
        "Do NOT assume the stack. Inspect the repo first (manifest, lock file, "
        "README) to find the right package manager and test command.\n"
        "You are on Windows (PowerShell). Only run commands needed to clone, "
        "install, and test — nothing else.\n"
        "End with one verdict line: 'TESTS PASSED' or 'TESTS FAILED'."
    ),
    tools=[ShellTools()],
    markdown=True,
    debug_mode=True,
)


async def main():
    await agent.aprint_response(
        "Run the tests for the GitHub repository "
        "https://github.com/SnirAbo/itp-habits-20260905"
    )


if __name__ == "__main__":
    asyncio.run(main())