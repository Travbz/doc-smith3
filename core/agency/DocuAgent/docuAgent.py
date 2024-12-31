from agency_swarm import Agent
from .tools.documentation_tools import (
    AnalyzeRepositoryTool,
    GenerateDocumentationTool,
    ReviewDocumentationTool
)

class DocuAgent(Agent):
    """Documentation agent responsible for analyzing code and generating documentation"""
    
    def __init__(self):
        super().__init__(
            name="DocuAgent",
            description="""Documentation expert agent that analyzes repositories and generates comprehensive documentation.
            Process:
            1. Use AnalyzeRepositoryTool to analyze the repository structure
            2. Use GenerateDocumentationTool with the analysis results
            3. Use ReviewDocumentationTool to verify the generated documentation
            
            Note: Always pass the complete analysis from AnalyzeRepositoryTool to GenerateDocumentationTool.""",
            instructions="instructions.md",
            tools=[
                AnalyzeRepositoryTool,
                GenerateDocumentationTool,
                ReviewDocumentationTool
            ],
            model="gpt-4-1106-preview"
        )