# server.py
from fastmcp import FastMCP
from orchestrator import run_pipeline

mcp = FastMCP("Idea-To-Prod")

#     Note: implementation currently wires only Agent 1-3 
#     end-to-end; agents 4-6 are being added incrementally.
@mcp.tool()
async def ideaToProd(idea: str) -> str:
    """Turns a natural-language application idea into fully generated,
    tested application code.

    Given an idea, this tool runs it end-to-end through a multi-agent
    pipeline:

    1. Creates a high-level design document for the application and
       saves it to Google Drive.
    2. Expands the high-level design into a detailed, phase-by-phase
       design document, saves it to Google Drive, and creates the
       corresponding development tasks as work items in Jira.
    3. Pulls the Jira tasks and generates the full application code,
       publishing it as a new GitHub repository.
    4. Generates unit tests for the generated code and saves them to
       the same GitHub repository. Uses a different model than the
       code-generation step.
    5. Executes the unit tests via Playwright. If any test fails, the
       pipeline loops back to step 4 to regenerate the tests until
       they pass.
    6. (Optional) Deploys the passing application to a live environment.

    Returns the final generated application code once all tests pass.
    """
    return await run_pipeline(idea)

if __name__ == "__main__":
    mcp.run()