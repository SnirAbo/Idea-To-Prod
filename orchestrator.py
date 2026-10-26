# orchestrator.py
import asyncio
import re

from dotenv import load_dotenv
from agents.agent1_hl_design import run_agent1
from agents.agent2_detailed_design import run_agent2
from agents.agent3_code_gen import run_agent3
from agents.agent4_unit_tests import run_agent4
from agents.agent5_test_execution import run_agent5

load_dotenv()


def extract_repo_url(text: str) -> str:
    match = re.search(r"https://github\.com/[\w.-]+/[\w.-]+", text)
    if not match:
        raise ValueError(f"No GitHub repo URL found in Agent 3 output:\n{text}")
    return match.group(0).rstrip("/.")


async def run_pipeline(idea: str):
    print("=== Agent 1: HL Design ===")
    hl_design = await run_agent1(idea)

    print("=== Agent 2: Detailed Design + Jira ===")
    await run_agent2(hl_design)

    print("=== Agent 3: Code Generation ===")
    agent3_output = await run_agent3()
    repo_url = extract_repo_url(agent3_output)
    print(f"Repo created: {repo_url}")

    print("=== Agent 4: Unit Tests ===")
    await run_agent4(repo_url)

    print("=== Agent 5: Test Execution ===")
    verdict = await run_agent5(repo_url)
    print(verdict)

    return verdict


if __name__ == "__main__":
    idea = input("Enter your idea: ");
    asyncio.run(run_pipeline(idea))