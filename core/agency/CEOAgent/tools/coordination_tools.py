from agency_swarm.tools import BaseTool
import os
from typing import ClassVar

class CoordinateDocumentationTool(BaseTool):
    name: ClassVar[str] = "coordinate_documentation"
    description: ClassVar[str] = "Coordinate the documentation generation process"
    
    def run(self, repo_url: str, github_token: str, branch_name: str) -> dict:
        try:
            # The LLM coordinates between agents, we just validate inputs
            if not github_token:
                return {"success": False, "error": "GitHub token required"}
            if not repo_url.startswith(("http://", "https://")):
                return {"success": False, "error": "Invalid repository URL"}
            
            return {
                "success": True,
                "message": "Documentation process initiated",
                "repo": repo_url,
                "branch": branch_name
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

class StatusCheckTool(BaseTool):
    name: ClassVar[str] = "check_status"
    description: ClassVar[str] = "Check if all required services are properly initialized"
    
    def run(self) -> dict:
        try:
            required_vars = ["OPENAI_API_KEY", "GITHUB_TOKEN"]
            missing = [var for var in required_vars if not os.getenv(var)]
            
            return {
                "success": len(missing) == 0,
                "message": "All systems operational" if not missing else f"Missing: {', '.join(missing)}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}