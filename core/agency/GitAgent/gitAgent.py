from agency_swarm import Agent
from .tools.git_tools import (
    CloneRepositoryTool,
    CreateBranchTool,
    CommitChangesTool,
    PushChangesTool,
    CreatePullRequestTool
)
import os
from ..settings.settings import GIT_AGENT_ID, DEFAULT_MODEL, AGENT_SETTINGS, GITHUB_TOKEN

class GitAgent(Agent):
    def __init__(self):
        # Validate GitHub token
        github_token = GITHUB_TOKEN or os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN must be set in settings or environment")

        super().__init__(
            name="GitAgent",
            description="""Expert in Git operations. I handle:
                - Cloning repositories
                - Creating branches
                - Committing changes
                - Pushing updates
                - Creating pull requests
                
                I use settings or environment variables for authentication.""",
            instructions="instructions.md",
            tools=[
                CloneRepositoryTool,
                CreateBranchTool,
                CommitChangesTool,
                PushChangesTool,
                CreatePullRequestTool
            ],
            model=AGENT_SETTINGS.get("model", DEFAULT_MODEL),
            temperature=AGENT_SETTINGS.get("temperature", 0.3),
            id=GIT_AGENT_ID
        )