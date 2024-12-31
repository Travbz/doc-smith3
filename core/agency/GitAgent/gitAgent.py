from agency_swarm import Agent
from .tools.git_tools import (
    CloneRepositoryTool,
    CreateBranchTool,
    CommitChangesTool,
    PushChangesTool,
    CreatePullRequestTool
)
import os

class GitAgent(Agent):
    def __init__(self):
        # Validate GitHub token
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN environment variable must be set")

        super().__init__(
            name="GitAgent",
            description="""Expert in Git operations. I handle:
                - Cloning repositories
                - Creating branches
                - Committing changes
                - Pushing updates
                - Creating pull requests
                
                I use environment variables for authentication, so tokens should never be passed directly.""",
            instructions="instructions.md",
            tools=[
                CloneRepositoryTool,
                CreateBranchTool,
                CommitChangesTool,
                PushChangesTool,
                CreatePullRequestTool
            ],
            model="gpt-4-1106-preview"
        )