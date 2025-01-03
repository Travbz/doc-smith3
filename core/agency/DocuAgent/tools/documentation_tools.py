from agency_swarm.tools import BaseTool
from pathlib import Path
import os
from typing import Dict, Any, List, ClassVar, Set, Optional
from pydantic import Field, BaseModel, validator
from ...settings.settings import (
    DOCS_OUTPUT_DIR,
    IGNORE_DIRS,
    DOCS_INDEX_FILE,
    README_FILE,
    FILES_DIR
)

class FileAnalysis(BaseModel):
    """Structure for analyzed file information"""
    path: str
    content: str
    size: int

class RepositoryAnalysis(BaseModel):
    """Complete repository analysis structure"""
    files: List[FileAnalysis]
    repo_path: str

class AnalyzeRepositoryTool(BaseTool):
    """Repository analyzer that leverages LLM capabilities for deep understanding"""
    name: ClassVar[str] = "analyze_repository"
    description: ClassVar[str] = """Analyze repository content using LLM capabilities for deep semantic understanding.
    Reads and analyzes all files in the repository to inform documentation generation."""
    
    repo_path: str = Field(description="Full path to the repository to analyze")

    def run(self) -> dict:
        try:
            repo_path = Path(self.repo_path)
            if not repo_path.exists():
                return {"success": False, "error": f"Repository path does not exist: {self.repo_path}"}

            # Analyze all files in the repository
            analyzed_files = []
            for root, _, files in os.walk(repo_path):
                rel_root = Path(root).relative_to(repo_path)
                
                # Skip ignored directories
                if any(part.startswith('.') for part in rel_root.parts):
                    continue
                if any(part in IGNORE_DIRS for part in rel_root.parts):
                    continue
                
                for file in files:
                    file_path = Path(root) / file
                    try:
                        # Get relative path
                        rel_path = file_path.relative_to(repo_path)
                        
                        # Skip compiled files and artifacts
                        if file_path.suffix in {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.class'}:
                            continue
                            
                        # Read the entire file
                        content = file_path.read_text(errors='ignore')
                        
                        analyzed_files.append(FileAnalysis(
                            path=str(rel_path),
                            content=content,
                            size=len(content)
                        ))
                    except Exception as e:
                        print(f"Error reading {file_path}: {str(e)}")

            analysis = RepositoryAnalysis(
                files=analyzed_files,
                repo_path=str(repo_path)
            )

            return {
                "success": True,
                "analysis": analysis.model_dump()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

class GenerateDocumentationTool(BaseTool):
    """Documentation generator that leverages LLM capabilities"""
    name: ClassVar[str] = "generate_documentation"
    description: ClassVar[str] = """Generate documentation based on repository analysis and optional review feedback."""
    
    analysis: dict = Field(description="Complete repository analysis from AnalyzeRepositoryTool")
    repo_path: str = Field(description="Repository path")
    review_feedback: Optional[dict] = Field(
        description="Optional feedback from ReviewAgent",
        default=None
    )

    def run(self) -> dict:
        try:
            repo_path = Path(self.repo_path)
            docs_dir = repo_path / DOCS_OUTPUT_DIR
            docs_dir.mkdir(parents=True, exist_ok=True)

            # Process repository analysis
            repo_analysis = RepositoryAnalysis(**self.analysis)
            
            # Generate documentation based on analysis and any feedback
            generated_docs = self._generate_documentation(
                repo_analysis,
                self.review_feedback
            )
            
            # Write documentation files
            written_files = []
            for doc_path, content in generated_docs.items():
                try:
                    # Handle special files
                    if doc_path == "README.md":
                        full_path = repo_path / README_FILE
                    elif doc_path == "index.md":
                        full_path = docs_dir / DOCS_INDEX_FILE
                    else:
                        full_path = docs_dir / doc_path
                    
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    full_path.write_text(content)
                    written_files.append(str(full_path.relative_to(repo_path)))
                except Exception as e:
                    print(f"Error writing {doc_path}: {str(e)}")

            return {
                "success": True,
                "docs_dir": str(docs_dir),
                "generated_files": written_files
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _generate_documentation(self, analysis: RepositoryAnalysis, 
                              review_feedback: Optional[dict]) -> Dict[str, str]:
        """Generate documentation based on analysis and feedback"""
        docs = {}
        
        # Let LLM analyze files to determine what documentation is needed
        for file in analysis.files:
            # Process files to determine documentation needs
            # The LLM can look at file content, patterns, and structure
            # to decide what documentation to generate
            pass  # LLM will implement actual generation
            
        # If we have review feedback, incorporate it
        if review_feedback:
            # Let LLM process feedback and adjust documentation
            pass  # LLM will implement feedback incorporation

        return docs  # LLM will return actual generated documentation