from agency_swarm import Agent
from .tools.coordination_tools import CoordinateDocumentationTool, StatusCheckTool
from ..settings.settings import CEO_AGENT_ID, DEFAULT_MODEL, AGENT_SETTINGS

class CEOAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CEOAgent",
            description="Coordination agent for documentation generation",
            instructions="instructions.md",
            tools=[CoordinateDocumentationTool, StatusCheckTool],
            model=AGENT_SETTINGS.get("model", DEFAULT_MODEL),
            temperature=AGENT_SETTINGS.get("temperature", 0.3),
            id=CEO_AGENT_ID
        )