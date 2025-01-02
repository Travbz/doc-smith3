from agency_swarm import Agency
from core.agency.GitAgent.gitAgent import GitAgent
from core.agency.DocuAgent.docuAgent import DocuAgent
from core.agency.ReviewAgent.reviewAgent import ReviewAgent
import os
from typing import Optional
import typer
from pathlib import Path
from datetime import datetime
from rich.console import Console
from core.agency.agency import create_agency
from core.agency.settings.settings import (
    OPENAI_API_KEY,
    GITHUB_TOKEN,
    DEFAULT_MODEL,
    AGENT_SETTINGS,
    DOCS_OUTPUT_DIR,
    FILES_DIR
)

console = Console()
app = typer.Typer()

class SafeFormatter:
    @staticmethod
    def clean_sensitive_data(text: str) -> str:
        # Get token to remove
        token = GITHUB_TOKEN or os.getenv("GITHUB_TOKEN", "")
        if token and token in text:
            text = text.replace(token, "***")
        return text

@app.command()
def generate_docs(
    repo_url: str = typer.Argument(..., help="GitHub repository URL"),
    github_token: Optional[str] = typer.Option(
        None,
        help="GitHub token. If not provided, will use GITHUB_TOKEN from settings or environment"
    ),
    review_iterations: int = typer.Option(
        3,
        help="Maximum number of review iterations"
    )
) -> None:
    """Generate and review documentation for a GitHub repository"""
    # Ensure settings directory exists
    Path(FILES_DIR).mkdir(parents=True, exist_ok=True)
    Path(DOCS_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Check OpenAI API key
    api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
    if not api_key:
        typer.echo("Error: OPENAI_API_KEY not found in settings or environment")
        raise typer.Exit(1)
    if api_key == "your-openai-key":
        typer.echo("Error: OPENAI_API_KEY not configured. Please set your actual API key")
        raise typer.Exit(1)

    # Check GitHub token
    token = github_token or GITHUB_TOKEN or os.getenv("GITHUB_TOKEN")
    if not token:
        typer.echo("Error: GitHub token not provided in settings, environment, or command line")
        raise typer.Exit(1)
    if token == "your-github-token":
        typer.echo("Error: GITHUB_TOKEN not configured. Please set your actual GitHub token")
        raise typer.Exit(1)

    # Create agency using settings
    console.print("[bold blue]Creating documentation agency...[/]")
    agency = create_agency()

    try:
        # Start the documentation process with review iterations
        console.print(f"[bold green]Starting documentation process for {repo_url}...[/]")
        
        prompt = f"""Please analyze and document the repository at {repo_url}.

        Process:
        1. Generate documentation:
           - Analyze repository structure and content
           - Create comprehensive documentation
           - Focus on clarity and completeness
           - Include code examples where relevant
           - Document architecture and design decisions
           
        2. Review and improve:
           - Review documentation quality and coverage
           - Identify any gaps or unclear sections
           - Provide specific improvement recommendations
           - Iterate up to {review_iterations} times until quality standards are met

        3. Quality Standards:
           - Documentation is complete and accurate
           - All major components are documented
           - Examples are clear and working
           - Architecture is well-explained
           - Setup instructions are complete
           - API documentation is comprehensive
           
        Note: Git operations will be handled automatically by the GitAgent.
        Working directory: {FILES_DIR}
        Documentation output: {DOCS_OUTPUT_DIR}
        """

        # Get messages with yield for progress tracking
        result_gen = agency.get_completion(
            message=SafeFormatter.clean_sensitive_data(prompt),
            yield_messages=True
        )

        try:
            for message in result_gen:
                # Clean any sensitive data before printing
                if hasattr(message, 'content'):
                    message.content = SafeFormatter.clean_sensitive_data(str(message.content))
                # Print each message as it arrives
                message.cprint()
        except StopIteration as e:
            # Get the final result
            result = e.value
            # Clean any sensitive data from result
            result = SafeFormatter.clean_sensitive_data(str(result))
            console.print(f"\n[bold green]Documentation generated and reviewed successfully![/]")
            console.print(f"[bold]Result:[/] {result}")
        
    except Exception as e:
        # Clean any sensitive data from error message
        error_msg = SafeFormatter.clean_sensitive_data(str(e))
        console.print(f"[bold red]Error:[/] {error_msg}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()