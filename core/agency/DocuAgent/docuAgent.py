from agency_swarm import Agent
from .tools.documentation_tools import (
    AnalyzeRepositoryTool,
    GenerateDocumentationTool
)

class DocuAgent(Agent):
    """Documentation agent responsible for analyzing code and generating documentation"""
    
    def __init__(self):
        super().__init__(
            name="DocuAgent",
            description="Documentation expert agent that analyzes repositories and generates comprehensive documentation. Specializes in repository analysis, documentation generation, and quality review using LLM capabilities.",
            instructions="instructions.md",
            tools=[
                AnalyzeRepositoryTool,
                GenerateDocumentationTool
            ],
            model="gpt-4-1106-preview"
        )