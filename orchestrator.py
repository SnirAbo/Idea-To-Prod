from agents.agent1_hl_design import run_agent1
from agents.agent2_detailed_design import run_agent2
from agents.agent3_code_gen import run_agent3

async def run_pipeline(idea: str) -> str:
    hl_design_ref = await run_agent1(idea)
    detailed_design_response = await run_agent2(hl_design_ref)
    code_repo_url = await run_agent3()

    return code_repo_url