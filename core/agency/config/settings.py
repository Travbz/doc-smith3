import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Agent IDs (can be used to reuse existing assistants)
CEO_AGENT_ID = os.getenv("CEO_AGENT_ID")
GIT_AGENT_ID = os.getenv("GIT_AGENT_ID")
DOCU_AGENT_ID = os.getenv("DOCU_AGENT_ID")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-4-1106-preview"

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# File paths
FILES_DIR = BASE_DIR / "files"
DOCS_OUTPUT_DIR = FILES_DIR / "docs"

# Documentation settings
DOCS_INDEX_FILE = "index.md"
README_FILE = "README.md"

# Repository Analysis Settings
IGNORE_DIRS = {
    '.git', '__pycache__', 'node_modules', 
    'venv', '.venv', 'build', 'dist'
}

DEPENDENCY_FILES = {
    'requirements.txt': 'python',
    'package.json': 'javascript',
    'Gemfile': 'ruby',
    'pom.xml': 'java',
    'build.gradle': 'java',
    'Cargo.toml': 'rust'
}

# Agent Settings (shared configuration for agency-swarm)
AGENT_SETTINGS = {
    "temperature": 0.3,
    "model": DEFAULT_MODEL,
    "files_folder": str(FILES_DIR),
}