from agency_swarm.tools import BaseTool
from pathlib import Path
from typing import ClassVar, Dict, List, Any
from pydantic import Field

class AnalyzeDocumentationCoverageAndQualityTool(BaseTool):
    """Analyze documentation completeness and quality"""
    name: ClassVar[str] = "analyze_documentation"
    description: ClassVar[str] = """Analyze documentation for completeness, clarity, and quality.
    Performs deep analysis of documentation content and structure."""
    
    docs_dir: str = Field(description="Directory containing documentation to analyze")
    codebase_dir: str = Field(description="Directory containing the source code")

    def run(self) -> dict:
        try:
            docs_path = Path(self.docs_dir)
            code_path = Path(self.codebase_dir)
            
            if not docs_path.exists():
                return {"success": False, "error": "Documentation directory not found"}
            if not code_path.exists():
                return {"success": False, "error": "Codebase directory not found"}

            # Analyze documentation files
            doc_files = {}
            for file_path in docs_path.rglob("*.md"):
                try:
                    content = file_path.read_text()
                    doc_files[str(file_path)] = content
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")

            analysis = {
                "files": doc_files,
                "codebase_path": str(code_path)
            }

            return {
                "success": True,
                "analysis": analysis
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

class ValidateAgainstCodebaseTool(BaseTool):
    """Cross-reference documentation with codebase"""
    name: ClassVar[str] = "validate_against_code"
    description: ClassVar[str] = """Validate documentation accuracy against actual codebase.
    Cross-references examples, APIs, and architectural descriptions."""
    
    analysis: dict = Field(description="Documentation analysis from AnalyzeDocumentationCoverageAndQualityTool")

    def run(self) -> dict:
        try:
            doc_files = self.analysis["files"]
            codebase_path = Path(self.analysis["codebase_path"])

            # Read relevant code files
            code_files = {}
            for ext in ['.py', '.js', '.ts', '.jsx', '.tsx']:
                for file_path in codebase_path.rglob(f"*{ext}"):
                    try:
                        content = file_path.read_text()
                        code_files[str(file_path)] = content
                    except Exception as e:
                        print(f"Error reading {file_path}: {str(e)}")

            validation = {
                "documentation": doc_files,
                "codebase": code_files
            }

            return {
                "success": True,
                "validation": validation
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

class ProvideFeedbackTool(BaseTool):
    """Generate specific, actionable documentation feedback"""
    name: ClassVar[str] = "provide_feedback"
    description: ClassVar[str] = """Generate detailed, actionable feedback on documentation.
    Provides specific recommendations for improvements."""
    
    validation: dict = Field(description="Validation results from ValidateAgainstCodebaseTool")

    def run(self) -> dict:
        try:
            doc_files = self.validation["documentation"]
            code_files = self.validation["codebase"]

            # Let LLM generate detailed feedback
            feedback = {
                "status": self._determine_status(doc_files, code_files),
                "critical_issues": self._find_critical_issues(doc_files, code_files),
                "improvements": self._suggest_improvements(doc_files, code_files),
                "metrics": self._calculate_metrics(doc_files)
            }

            return {
                "success": True,
                "feedback": feedback
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _determine_status(self, doc_files: Dict[str, str], code_files: Dict[str, str]) -> str:
        """Determine overall documentation status"""
        return "needs_review"  # Placeholder for LLM determination

    def _find_critical_issues(self, doc_files: Dict[str, str], 
                            code_files: Dict[str, str]) -> List[Dict[str, str]]:
        """Identify critical documentation issues"""
        return []  # Placeholder for LLM analysis

    def _suggest_improvements(self, doc_files: Dict[str, str], 
                            code_files: Dict[str, str]) -> List[Dict[str, str]]:
        """Suggest documentation improvements"""
        return []  # Placeholder for LLM suggestions

    def _calculate_metrics(self, doc_files: Dict[str, str]) -> Dict[str, Any]:
        """Calculate documentation quality metrics"""
        return {}  # Placeholder for LLM metrics