# Doc-Smith3: AI-Powered Documentation Generator

An intelligent documentation generation system using LLMs and agent-based architecture to create comprehensive documentation for code repositories.

## Project Structure

```
core/
├── agency/
│   ├── config/
│   │   └── settings.py         # Centralized configuration
│   ├── docuAgent/
│   │   ├── prompts/           # LLM instruction files
│   │   ├── schemas/           # Data structure definitions
│   │   └── tools/             # Documentation tools
│   └── gitAgent/
       ├── prompts/            # Git operation instructions
       ├── schemas/            # Git operation structures
       └── tools/              # Git management tools
```

## Current Status

### Completed Components ✅

1. Configuration System
   - Centralized settings in `settings.py`
   - Model configuration per agent/tool
   - Environment variable management
   - Dependency configurations

2. Documentation Agent Tools
   - Content generator with prompt loading
   - File system operations
   - Markdown generation structure
   - Component identification

3. Prompt System
   - System prompts in markdown files
   - User prompts for documentation
   - Review prompts for validation

4. Basic Project Structure
   - Agent-based architecture
   - Tool organization
   - Prompt management

### Work In Progress 🚧

1. Git Agent Implementation
   - Repository operations
   - Branch management
   - Pull request handling

2. Documentation Agent Tools
   - Repository analyzer
   - Content reviser
   - Feedback processor

3. Integration
   - Agent communication
   - End-to-end workflow
   - Error handling

### Not Started Yet 📝

1. Main Application Flow
   - Workflow orchestration
   - Command line interface
   - Progress reporting

2. Documentation Templates
   - Language-specific templates
   - Project type templates
   - Custom template support

3. Testing and Validation
   - Basic error handling
   - Input validation
   - Output verification

## Usage

Currently in development. Basic setup:

```bash
# Clone repository
git clone [repository-url]

# Run setup script
./setup.sh

# Activate environment
source .venv/bin/activate
```

## LLM Configuration

The system uses different GPT models for various tasks:

- Documentation Generation: GPT-4-turbo-preview
- Repository Analysis: GPT-3.5-turbo
- Git Operations: GPT-3.5-turbo

Configure model settings in `core/agency/config/settings.py`.

## Environment Setup

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `GITHUB_TOKEN`: GitHub Personal Access Token

## Next Steps

1. Complete the GitAgent implementation
2. Develop remaining DocumentationAgent tools
3. Implement main workflow
4. Add template system
5. Create CLI interface

## Contributing

Project is in active development. Pull requests welcome!


python -m core.main "https://github.com/username/repo"

python -m core.main "https://github.com/Travbz/consensus-engine"