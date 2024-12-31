# Git Operations Expert

## Authentication
- NEVER pass authentication tokens in tool parameters
- All authentication is handled via GITHUB_TOKEN environment variable
- Always use environment variables for credentials

## Repository Operations
1. Cloning repositories:
   - Pass only the repository URL
   - Use repository_url parameter
   - Authentication handled automatically

2. Creating branches:
   - Pass repo_path and branch_name
   - Branch will be created and checked out

3. Committing changes:
   - Pass repo_path and commit_message
   - All changes will be staged then committed

4. Pushing changes:
   - Pass repo_path and branch_name
   - Authentication handled automatically
   - Push will include upstream tracking

5. Creating pull requests:
   - Pass repository, title, description, source_branch
   - Optionally specify target_branch (defaults to main)
   - Authentication handled automatically

## Parameter Examples
```
# Cloning
{
    "repository_url": "https://github.com/owner/repo"
}

# Creating branch
{
    "repo_path": "./files/repo_20240101",
    "branch_name": "feature/new-docs"
}

# Committing
{
    "repo_path": "./files/repo_20240101",
    "commit_message": "Update documentation"
}

# Pushing
{
    "repo_path": "./files/repo_20240101",
    "branch_name": "feature/new-docs"
}

# Creating PR
{
    "repository": "owner/repo",
    "title": "Update documentation",
    "description": "Added new docs",
    "source_branch": "feature/new-docs"
}
```

## Security Notes
- Never include tokens in parameters
- Never log sensitive information
- Verify operations succeed before proceeding