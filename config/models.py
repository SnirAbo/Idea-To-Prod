from agno.models.openai import OpenAIResponses
from agno.models.anthropic import Claude

HL_DESIGN_MODEL = OpenAIResponses(id="gpt-5")
DETAILED_DESIGN_MODEL = OpenAIResponses(id="gpt-5")
CODE_GEN_MODEL = OpenAIResponses(id="gpt-5")
UNIT_TEST_MODEL = Claude(id="claude-sonnet-5", max_tokens=16000) 
TEST_EXEC_MODEL = Claude(id="claude-haiku-4-5")
