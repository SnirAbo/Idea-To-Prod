import asyncio
import os
from dotenv import load_dotenv
from agno.agent import Agent
from config.models import UNIT_TEST_MODEL
from mcp_servers import get_github_tools 

load_dotenv()  

github_tools = get_github_tools();

agent = Agent(
    name="Unit Testing Agent",
    model=UNIT_TEST_MODEL,
    instructions=(
    "You are a QA engineer. You write automated tests for an existing web "
    "application whose code lives in a GitHub repository. Your PRIMARY goal "
    "is to WRITE and PUSH test files — not to analyze the codebase "
    "exhaustively.\n\n"

    "WORKFLOW — follow this order strictly:\n"
    "1. Read ONLY these to understand the app: the README, and the specific "
    "source files that contain the core logic you will test (for a habit "
    "tracker, that means the streak/completion logic and the date/schedule "
    "helpers). Read at most 6-8 files total. Do NOT explore the entire "
    "repository, do NOT read config files, CI files, or UI components you "
    "won't test.\n"
    "2. As SOON as you understand a piece of logic, write a test file for it "
    "and push it to the repository IMMEDIATELY using your GitHub tools "
    "(create_or_update_file). Do not wait until you have written all tests — "
    "push each test file the moment it is ready, then move to the next.\n"
    "3. Repeat until the core functionality is covered.\n\n"

    "RULES:\n"
    "- Do NOT modify, rewrite, or delete any existing source code. You only "
    "ADD test files.\n"
    "- Push each file as you go. Never batch all your work into one final "
    "step.\n"
    "- When finished, report which test files you created."
    ),
    tools=[github_tools],
    markdown=True,
    debug_mode=True,
)

# async def run_agent3() -> str:
#     async with github_tools:
#         response = await agent.arun(f"Jira project key: {JIRA_PROJECT_KEY}")
#         return response.content



async def main():
    print("TOKEN:", os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN", "MISSING"))
    async with github_tools:
        await agent.aprint_response(
        "Write tests for the GitHub repository SnirAbo/itp-habits-20260905."
        )


if __name__ == "__main__":
    asyncio.run(main())