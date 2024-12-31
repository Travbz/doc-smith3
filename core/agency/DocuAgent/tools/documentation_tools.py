from agency_swarm.tools import BaseTool
from pathlib import Path
import os
import json
from typing import Dict, Any, List, ClassVar, Set
from pydantic import Field, BaseModel

class RepoAnalysis(BaseModel):
    """Structure for repository analysis results"""
    file_structure: Dict[str, List[str]]
    file_extensions: Dict[str, int]
    file_samples: Dict[str, str]
    configuration_files: Dict[str, str]

class AnalyzeRepositoryTool(BaseTool):
    """Analyze repository structure and identify its key characteristics"""
    name: ClassVar[str] = "analyze_repository"
    description: ClassVar[str] = """Analyze repository structure and content. 
    IMPORTANT: Save the analysis result to pass to GenerateDocumentationTool.
    
    Example flow:
    ```python
    # First, analyze the repository
    result = analyze_repository(repo_path="path/to/repo")
    
    # Save the analysis for the next step
    analysis = result["analysis"]
    repo_path = result["repo_path"]
    
    # Then pass BOTH to generate_documentation
    docs = generate_documentation(
        analysis=analysis,
        repo_path=repo_path
    )
    ```
    """
    
    # Input parameter
    repo_path: str = Field(
        description="Full path to the repository to analyze"
    )
    
    # Class level configuration
    ignore_dirs: ClassVar[Set[str]] = {'.git', '__pycache__', 'node_modules', 'venv', '.venv', 'build', 'dist'}

    def run(self) -> dict:
        try:
            repo_path = Path(self.repo_path)
            if not repo_path.exists():
                return {"success": False, "error": f"Repository path does not exist: {self.repo_path}"}

            # Get all files and their extensions
            files_by_extension = {}
            for root, _, files in os.walk(repo_path):
                if any(ignore in root for ignore in self.ignore_dirs):
                    continue
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext:
                        if ext not in files_by_extension:
                            files_by_extension[ext] = []
                        files_by_extension[ext].append(os.path.join(root, file))

            # Sample the first file of each extension
            file_samples = {}
            for ext, files in files_by_extension.items():
                try:
                    with open(files[0], 'r', encoding='utf-8') as f:
                        # Get first 1000 characters as a sample
                        file_samples[ext] = f.read(1000)
                except:
                    continue

            # Get basic repo analysis
            analysis = RepoAnalysis(
                file_structure=self._analyze_structure(repo_path),
                file_extensions=dict([(ext, len(files)) 
                                  for ext, files in files_by_extension.items()]),
                file_samples=file_samples,
                configuration_files=self._find_config_files(repo_path)
            )

            return {
                "success": True, 
                "analysis": analysis.model_dump(),
                "repo_path": str(repo_path),
                "message": "Repository analyzed successfully. Pass this analysis to GenerateDocumentationTool."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _analyze_structure(self, path: Path) -> Dict[str, List[str]]:
        """Get repository directory structure"""
        structure = {}
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            if not any(ignore in root for ignore in self.ignore_dirs):
                rel_path = os.path.relpath(root, path)
                if rel_path == '.':
                    rel_path = 'root'
                structure[rel_path] = files
        return structure

    def _find_config_files(self, path: Path) -> Dict[str, str]:
        """Find and read configuration files"""
        config_patterns = {
            'package.json': 'Node.js/JavaScript',
            'requirements.txt': 'Python',
            'pyproject.toml': 'Python',
            'setup.py': 'Python',
            'Cargo.toml': 'Rust',
            'pom.xml': 'Java/Maven',
            'build.gradle': 'Java/Gradle',
            'Gemfile': 'Ruby',
            'composer.json': 'PHP',
            '.env.example': 'Environment',
            'docker-compose.yml': 'Docker',
            'Dockerfile': 'Docker'
        }

        config_files = {}
        for root, _, files in os.walk(path):
            if any(ignore in root for ignore in self.ignore_dirs):
                continue
            for file in files:
                if file in config_patterns:
                    try:
                        with open(os.path.join(root, file), 'r') as f:
                            config_files[file] = f.read()
                    except:
                        continue
        return config_files

class GenerateDocumentationTool(BaseTool):
    """Generate comprehensive documentation based on repository analysis"""
    name: ClassVar[str] = "generate_documentation"
    description: ClassVar[str] = """Generate comprehensive documentation based on repository analysis.
    REQUIRES the complete analysis dictionary from AnalyzeRepositoryTool and the repo path.
    
    Expected parameters:
    1. analysis: The complete analysis dictionary from AnalyzeRepositoryTool's result
    2. repo_path: The repository path from AnalyzeRepositoryTool's result
    
    Example correct usage:
    ```python
    # First get analysis result
    analyze_result = analyze_repository(repo_path="path/to/repo")
    
    # Then use BOTH analysis and repo_path
    generate_documentation(
        analysis=analyze_result["analysis"],  # Must pass the analysis dict
        repo_path=analyze_result["repo_path"]  # Must pass the repo path
    )
    ```
    
    Common errors:
    - Forgetting to pass the analysis dictionary
    - Passing wrong format for analysis
    - Not passing both required parameters
    """
    
    # Input parameters
    analysis: dict = Field(
        description="Complete analysis dictionary from AnalyzeRepositoryTool containing file_structure, file_extensions, file_samples, and configuration_files"
    )
    repo_path: str = Field(
        description="Path to the repository being documented"
    )

    def run(self) -> dict:
        try:
            # Create docs directory in repository
            repo_path = Path(self.repo_path)
            docs_dir = repo_path / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)

            # Convert analysis dict back to model for validation
            try:
                repo_analysis = RepoAnalysis(**self.analysis)
            except Exception as e:
                return {
                    "success": False, 
                    "error": f"Invalid analysis format. Make sure to pass the complete analysis from AnalyzeRepositoryTool: {str(e)}"
                }

            # Create documentation
            docs = {
                "README.md": self._generate_readme(repo_analysis),
                "CONTRIBUTING.md": self._generate_contributing(repo_analysis),
                "ARCHITECTURE.md": self._generate_architecture(repo_analysis),
                "API.md": self._generate_api_docs(repo_analysis),
            }

            # Write documentation files
            for filename, content in docs.items():
                file_path = docs_dir / filename
                file_path.write_text(content)

            return {
                "success": True,
                "docs_dir": str(docs_dir),
                "generated_files": list(docs.keys()),
                "message": "Documentation generated. Use ReviewDocumentationTool to verify."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _generate_readme(self, analysis: RepoAnalysis) -> str:
        readme = "# Project Documentation\n\n"
        readme += "## Project Structure\n\n```\n"
        for path, files in analysis.file_structure.items():
            readme += f"{path}/\n"
            for file in files:
                readme += f"  - {file}\n"
        readme += "```\n\n"

        # Add language information
        readme += "## Languages & Technologies\n\n"
        for ext, count in analysis.file_extensions.items():
            readme += f"- {ext}: {count} files\n"
        
        return readme

    def _generate_contributing(self, analysis: RepoAnalysis) -> str:
        contributing = "# Contributing Guidelines\n\n"
        contributing += "## Development Setup\n\n"
        if "requirements.txt" in analysis.configuration_files:
            contributing += "### Python Setup\n```bash\npip install -r requirements.txt\n```\n\n"
            # Extract requirements
            reqs = analysis.configuration_files["requirements.txt"].split("\n")
            contributing += "#### Dependencies:\n"
            for req in reqs:
                if req.strip():
                    contributing += f"* {req}\n"
        if "package.json" in analysis.configuration_files:
            contributing += "### Node.js Setup\n```bash\nnpm install\n```\n\n"
            # Extract package.json info
            try:
                pkg = json.loads(analysis.configuration_files["package.json"])
                if "dependencies" in pkg:
                    contributing += "#### Dependencies:\n"
                    for dep, ver in pkg["dependencies"].items():
                        contributing += f"* {dep}: {ver}\n"
            except:
                pass
        return contributing

    def _generate_architecture(self, analysis: RepoAnalysis) -> str:
        architecture = "# Architecture Overview\n\n"
        
        # Technology stack
        architecture += "## Technology Stack\n\n"
        for ext, count in analysis.file_extensions.items():
            architecture += f"- {ext}: {count} files\n"

        # Project structure
        architecture += "\n## Project Organization\n\n"
        for path, files in analysis.file_structure.items():
            if path == "root":
                architecture += "### Root Directory\n"
            else:
                architecture += f"### {path}\n"
            for file in files:
                architecture += f"- `{file}`\n"
            architecture += "\n"

        return architecture

    def _generate_api_docs(self, analysis: RepoAnalysis) -> str:
        api_docs = "# API Documentation\n\n"
        
        # Look for common API indicators
        api_patterns = {
            ".py": ["@app.route", "class", "def ", "async def"],
            ".js": ["app.get(", "app.post(", "router."],
            ".ts": ["@Controller", "@Injectable", "interface"]
        }

        for ext, patterns in api_patterns.items():
            if ext in analysis.file_samples:
                sample = analysis.file_samples[ext]
                if any(pattern in sample for pattern in patterns):
                    api_docs += f"## {ext} APIs\n\n"
                    api_docs += "API documentation will be generated based on code analysis.\n\n"

        return api_docs

class ReviewDocumentationTool(BaseTool):
    """Review generated documentation for completeness and quality"""
    name: ClassVar[str] = "review_documentation"
    description: ClassVar[str] = """Review generated documentation for completeness and quality.
    Use after GenerateDocumentationTool has created the documentation.
    
    Example flow:
    ```python
    # First generate docs
    docs_result = generate_documentation(...)
    
    # Then review using the docs directory
    review = review_documentation(docs_dir=docs_result["docs_dir"])
    ```
    """
    
    # Input parameter
    docs_dir: str = Field(
        description="Path to the documentation directory to review"
    )

    def run(self) -> dict:
        try:
            docs_path = Path(self.docs_dir)
            if not docs_path.exists():
                return {"success": False, "error": f"Documentation directory not found: {self.docs_dir}"}

            # Read all documentation files
            docs = {}
            for path in docs_path.rglob("*.md"):
                try:
                    docs[str(path.relative_to(docs_path))] = path.read_text()
                except:
                    continue

            # Validation checks
            required_files = {"README.md", "CONTRIBUTING.md", "ARCHITECTURE.md"}
            missing_files = required_files - set(docs.keys())
            
            checks = {
                "total_files": len(docs),
                "has_required_files": len(missing_files) == 0,
                "missing_files": list(missing_files),
                "file_list": list(docs.keys())
            }

            # Content checks
            content_checks = {}
            for file, content in docs.items():
                content_checks[file] = {
                    "word_count": len(content.split()),
                    "has_headings": content.count("#") > 0,
                    "has_code_blocks": "```" in content
                }

            return {
                "success": True,
                "files": docs,
                "stats": checks,
                "content_analysis": content_checks,
                "message": "Documentation review complete."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}