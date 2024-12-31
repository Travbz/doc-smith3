from agency_swarm.tools import BaseTool
import subprocess
import os
from pathlib import Path
from datetime import datetime
from github import Github
from typing import ClassVar, Dict, Optional
from pydantic import Field

class SafeFormatter:
    """Format strings while removing sensitive data"""
    @staticmethod
    def clean_sensitive_data(text: str) -> str:
        # Get token to remove
        token = os.getenv("GITHUB_TOKEN", "")
        if token and token in text:
            text = text.replace(token, "***")
        return text

class CloneRepositoryTool(BaseTool):
    """Clone a repository using GITHUB_TOKEN from environment"""
    name: ClassVar[str] = "clone_repository"
    description: ClassVar[str] = """Clone a GitHub repository.
    Authentication is handled automatically using GITHUB_TOKEN from environment.
    
    Example:
    ```python
    result = clone_repository(repository_url="https://github.com/owner/repo")
    repo_path = result["repo_path"]  # Save this for other operations
    ```
    """
    
    # Input parameter
    repository_url: str = Field(
        description="URL of the repository to clone (https://github.com/owner/repo format)"
    )

    def run(self) -> dict:
        try:
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                return {"success": False, "error": "GitHub token not found in environment"}

            # Create files directory if it doesn't exist
            files_dir = Path("files")
            files_dir.mkdir(exist_ok=True)
            
            # Create unique directory for this repo
            repo_name = self.repository_url.split('/')[-1].replace('.git', '')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            repo_dir = files_dir / f"{repo_name}_{timestamp}"
            repo_dir.mkdir(parents=True, exist_ok=True)

            # Clone with authentication but don't log the token
            auth_url = self.repository_url.replace('https://', f'https://{github_token}@')
            try:
                result = subprocess.run(
                    ['git', 'clone', auth_url, str(repo_dir)],
                    capture_output=True,
                    text=True,
                    check=True
                )
                # Clean any token from output
                safe_stdout = SafeFormatter.clean_sensitive_data(result.stdout)
                safe_stderr = SafeFormatter.clean_sensitive_data(result.stderr)
            except subprocess.CalledProcessError as e:
                # Clean any token from error output
                safe_stderr = SafeFormatter.clean_sensitive_data(e.stderr)
                return {"success": False, "error": f"Git clone failed: {safe_stderr}"}
            
            return {
                "success": True,
                "repo_path": str(repo_dir),
                "message": "Repository cloned successfully"
            }
        except Exception as e:
            error_msg = SafeFormatter.clean_sensitive_data(str(e))
            return {"success": False, "error": error_msg}

class CreateBranchTool(BaseTool):
    """Create and checkout a new branch"""
    name: ClassVar[str] = "create_branch"
    description: ClassVar[str] = """Create and checkout a new Git branch.
    
    Example:
    ```python
    result = create_branch(
        repo_path="/path/to/repo",
        branch_name="feature/new-docs"
    )
    ```
    """
    
    # Input parameters
    repo_path: str = Field(
        description="Path to repository"
    )
    branch_name: str = Field(
        description="Name for the new branch"
    )

    def run(self) -> dict:
        try:
            subprocess.run(
                ['git', 'checkout', '-b', self.branch_name],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            return {
                "success": True,
                "branch": self.branch_name,
                "message": f"Created and checked out branch: {self.branch_name}"
            }
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": f"Git error: {e.stderr}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

class CommitChangesTool(BaseTool):
    """Stage and commit all changes"""
    name: ClassVar[str] = "commit_changes"
    description: ClassVar[str] = """Stage and commit all changes in the repository.
    
    Example:
    ```python
    result = commit_changes(
        repo_path="/path/to/repo",
        commit_message="Update documentation"
    )
    ```
    """
    
    # Input parameters
    repo_path: str = Field(
        description="Path to repository"
    )
    commit_message: str = Field(
        description="Commit message"
    )

    def run(self) -> dict:
        try:
            # First add all changes
            subprocess.run(
                ['git', 'add', '.'],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Then commit
            subprocess.run(
                ['git', 'commit', '-m', self.commit_message],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            
            return {
                "success": True,
                "message": "Changes committed successfully"
            }
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": f"Git error: {e.stderr}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

class PushChangesTool(BaseTool):
    """Push changes to remote repository using GITHUB_TOKEN from environment"""
    name: ClassVar[str] = "push_changes"
    description: ClassVar[str] = """Push changes to remote repository.
    Authentication is handled automatically using GITHUB_TOKEN from environment.
    
    Example:
    ```python
    result = push_changes(
        repo_path="/path/to/repo",
        branch_name="feature/new-docs"
    )
    ```
    """
    
    # Input parameters
    repo_path: str = Field(
        description="Path to repository"
    )
    branch_name: str = Field(
        description="Branch to push"
    )

    def run(self) -> dict:
        try:
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                return {"success": False, "error": "GitHub token not found in environment"}

            # Get the current remote URL
            remote_url = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
            
            # Clean and format the remote URL
            base_url = remote_url.replace('https://', '').replace('http://', '')
            if '@' in base_url:
                base_url = base_url.split('@')[1]
            auth_url = f'https://{github_token}@{base_url}'
            
            # Set the authenticated remote URL
            try:
                subprocess.run(
                    ['git', 'remote', 'set-url', 'origin', auth_url],
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True,
                    text=True
                )

                # Push changes
                result = subprocess.run(
                    ['git', 'push', '-u', 'origin', self.branch_name],
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True,
                    text=True
                )
                # Clean any token from output
                safe_stdout = SafeFormatter.clean_sensitive_data(result.stdout)
                safe_stderr = SafeFormatter.clean_sensitive_data(result.stderr)
            except subprocess.CalledProcessError as e:
                safe_stderr = SafeFormatter.clean_sensitive_data(e.stderr)
                return {"success": False, "error": f"Git error: {safe_stderr}"}

            return {
                "success": True,
                "message": f"Changes pushed to {self.branch_name}"
            }
        except Exception as e:
            error_msg = SafeFormatter.clean_sensitive_data(str(e))
            return {"success": False, "error": error_msg}

class CreatePullRequestTool(BaseTool):
    """Create a new pull request using GITHUB_TOKEN from environment"""
    name: ClassVar[str] = "create_pull_request"
    description: ClassVar[str] = """Create a new pull request.
    Authentication is handled automatically using GITHUB_TOKEN from environment.
    
    Example:
    ```python
    result = create_pull_request(
        repository="owner/repo",
        title="Update documentation",
        description="Added comprehensive documentation",
        source_branch="feature/new-docs",
        target_branch="main"  # Optional, defaults to main
    )
    ```
    """
    
    # Input parameters
    repository: str = Field(
        description="Repository name in format 'owner/repo'"
    )
    title: str = Field(
        description="Pull request title"
    )
    description: str = Field(
        description="Pull request description"
    )
    source_branch: str = Field(
        description="Branch containing changes"
    )
    target_branch: str = Field(
        default="main",
        description="Base branch to merge into"
    )

    def run(self) -> dict:
        try:
            github_token = os.getenv("GITHUB_TOKEN")
            if not github_token:
                return {"success": False, "error": "GitHub token not found in environment"}

            gh = Github(github_token)
            repo = gh.get_repo(self.repository)
            
            pr = repo.create_pull(
                title=self.title,
                body=self.description,
                head=self.source_branch,
                base=self.target_branch
            )
            
            return {
                "success": True,
                "pr_url": pr.html_url,
                "pr_number": pr.number,
                "status": pr.state
            }
        except Exception as e:
            error_msg = SafeFormatter.clean_sensitive_data(str(e))
            return {"success": False, "error": error_msg}