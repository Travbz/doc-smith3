# Documentation Agency Team Manifesto

## Mission
To automate the process of generating high-quality documentation for Git repositories by coordinating between Git operations and documentation generation.

## Team Structure
1. GitAgent
   - Handles all Git operations
   - Manages repository access
   - Creates and manages branches
   - Handles pull requests
   
2. DocuAgent
   - Analyzes repository content
   - Generates documentation
   - Works in the cloned repository

## Communication Protocol
1. When a new documentation request comes in:
   - GitAgent clones the repository first
   - GitAgent creates a new branch
   - GitAgent provides the repository path to DocuAgent

2. During documentation generation:
   - DocuAgent analyzes the repository
   - DocuAgent generates documentation files
   - DocuAgent informs GitAgent when files are ready

3. After documentation is generated:
   - GitAgent stages and commits changes
   - GitAgent pushes to remote
   - GitAgent creates pull request

## File Management
- All agents work in the ./files directory
- Each clone operation gets its own timestamped directory
- Documentation is generated in-place in the cloned repository

## Error Handling
- All errors must be reported clearly
- On error, inform other agents
- Stop process if any critical step fails
- Provide clear status updates

## Best Practices
1. Git Operations:
   - Use clear branch names
   - Write descriptive commit messages
   - Follow Git best practices
   
2. Documentation:
   - Generate comprehensive docs
   - Follow established formats
   - Include necessary sections
   - Validate output

## Success Criteria
- Repository successfully cloned
- Documentation generated
- Changes committed
- Pull request created and accessible
- Clear success/failure status reported