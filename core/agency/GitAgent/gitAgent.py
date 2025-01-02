from agency_swarm import Agent
from .tools.git_tools import (
    CloneRepositoryTool,
    CreateBranchTool,
    CommitChangesTool,
    PushChangesTool,
    CreatePullRequestTool
)
import os
from datetime import datetime
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
                
                I automatically add timestamps to branch names and use environment variables for authentication.""",
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
    
    def create_timestamped_branch_name(self, base_name: str) -> str:
        """Create a branch name with timestamp"""
        # Format: docs/update-docs-YYYYMMDD-HHMM
        timestamp = datetime.now().strftime('%Y%m%d-%H%M')
        return f"{base_name}-{timestamp}"