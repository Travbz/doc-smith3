from agency_swarm import Agent
from .tools.review_tools import (
    AnalyzeDocumentationCoverageAndQualityTool,
    ValidateAgainstCodebaseTool,
    ProvideFeedbackTool
)
from ..settings.settings import REVIEW_AGENT_ID, DEFAULT_MODEL, AGENT_SETTINGS

class ReviewAgent(Agent):
    """Documentation review agent responsible for analyzing and validating documentation quality"""
    
    def __init__(self):
        super().__init__(
            name="ReviewAgent",
            description="""Documentation review expert that analyzes documentation quality and provides detailed feedback.
            Process:
            1. Analyze documentation coverage and quality
            2. Validate documentation against codebase
            3. Provide specific, actionable feedback
            4. Track and verify improvements""",
            instructions="instructions.md",
            tools=[
                AnalyzeDocumentationCoverageAndQualityTool,
                ValidateAgainstCodebaseTool,
                ProvideFeedbackTool
            ],
            model=AGENT_SETTINGS.get("model", DEFAULT_MODEL),
            temperature=AGENT_SETTINGS.get("temperature", 0.3),
            id=REVIEW_AGENT_ID
        )