from agency_swarm import Agency
from core.agency.GitAgent.gitAgent import GitAgent
from core.agency.DocuAgent.docuAgent import DocuAgent
import os
from typing import Optional
import typer
from pathlib import Path
from datetime import datetime
from rich.console import Console

console = Console()
app = typer.Typer()

class SafeFormatter:
    @staticmethod
    def clean_sensitive_data(text: str) -> str:
        # Get token to remove
        token = os.getenv("GITHUB_TOKEN", "")
        if token and token in text:
            text = text.replace(token, "***")
        return text

def create_agency() -> Agency:
    """Create and configure the documentation agency"""
    # Initialize agents
    git_agent = GitAgent()
    docu_agent = DocuAgent()

    # Create agency with communication paths
    # The format is [agent1, agent2] for connection between agents
    return Agency(
        [
            git_agent, docu_agent,  # Define the agents
            [git_agent, docu_agent]  # Define communication paths between agents
        ],
        shared_instructions='core/agency/agency-manifesto.md',
        temperature=0.3
    )

@app.command()
def generate_docs(
    repo_url: str = typer.Argument(..., help="GitHub repository URL"),
    github_token: Optional[str] = typer.Option(
        None,
        help="GitHub token. If not provided, will use GITHUB_TOKEN environment variable"
    )
) -> None:
    """Generate documentation for a GitHub repository"""
    # Check OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        typer.echo("Error: OPENAI_API_KEY environment variable not set")
        raise typer.Exit(1)
    if openai_key == "your-openai-key":
        typer.echo("Error: OPENAI_API_KEY not configured. Please set your actual API key")
        raise typer.Exit(1)

    # Check GitHub token
    token = github_token or os.getenv("GITHUB_TOKEN")
    if not token:
        typer.echo("Error: GitHub token not provided. Either pass --github-token or set GITHUB_TOKEN environment variable")
        raise typer.Exit(1)
    if token == "your-github-token":
        typer.echo("Error: GITHUB_TOKEN not configured. Please set your actual GitHub token")
        raise typer.Exit(1)

    # Create agency
    console.print("[bold blue]Creating documentation agency...[/]")
    agency = create_agency()

    # Extract repo name for branch naming
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    branch_name = f"docs/update-docs-{timestamp}"

    try:
        # Start the documentation process
        console.print(f"[bold green]Starting documentation process for {repo_url}...[/]")
        
        prompt = f"""Please generate documentation for the repository at {repo_url}.

        Steps:
        1. Clone the repository using the GitAgent
        2. Analyze the repository using DocuAgent
        3. Generate comprehensive documentation 
        4. Create a new branch named {branch_name}
        5. Commit the documentation changes
        6. Push the changes and create a pull request

        Note: GitHub authentication is handled via environment variables. Do not pass tokens in parameters.

        The final output should be a pull request URL."""

        # Get messages with yield so we can print them as they come
        result_gen = agency.get_completion(
            message=SafeFormatter.clean_sensitive_data(prompt),
            yield_messages=True  # Enable message streaming
        )

        try:
            for message in result_gen:
                # Clean any sensitive data before printing
                if hasattr(message, 'content'):
                    message.content = SafeFormatter.clean_sensitive_data(str(message.content))
                # Print each message as it arrives
                message.cprint()
        except StopIteration as e:
            # Get the final result from StopIteration
            result = e.value
            # Clean any sensitive data from result
            result = SafeFormatter.clean_sensitive_data(str(result))
            console.print(f"\n[bold green]Documentation generated successfully![/]")
            console.print(f"[bold]Result:[/] {result}")
        
    except Exception as e:
        # Clean any sensitive data from error message
        error_msg = SafeFormatter.clean_sensitive_data(str(e))
        console.print(f"[bold red]Error:[/] {error_msg}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()