from agency_swarm import Agent
from .tools.coordination_tools import CoordinateDocumentationTool, StatusCheckTool

class CEOAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CEOAgent",
            description="Coordination agent for documentation generation",
            instructions="instructions.md",
            tools=[CoordinateDocumentationTool, StatusCheckTool],
            model="gpt-4-1106-preview"
        )