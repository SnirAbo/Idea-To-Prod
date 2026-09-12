import asyncio
import sys

from dotenv import load_dotenv
from agno.agent import Agent
from config.models import HL_DESIGN_MODEL
from mcp_servers import get_drive_tools

load_dotenv()  # Load environment variables from .env file

drive_tools = get_drive_tools();

agent = Agent(
    name="HL Design Agent",
    model=HL_DESIGN_MODEL,
    instructions=(
        "You are a helpful assistant that provides high-level design suggestions "
        "for software projects. You will be given a project description and you "
        "should provide a detailed design outline, including architecture, "
        "components, and technologies to use. After creating the design, save it "
        "as a document in Google Drive using the available tools."
    ),
    tools=[drive_tools],
    markdown=True,
)


async def run_agent1(idea: str) -> str:
    async with drive_tools:
        response = await agent.arun(f"Idea: {idea}")
        return response.content


if __name__ == "__main__":
    idea = sys.argv[1] if len(sys.argv) > 1 else input("Enter an app idea: ")
    result = asyncio.run(run_agent1(idea))
    print(result)