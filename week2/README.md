# Action Item Extractor (Week 2)
This project is an AI-powered tool to extract tasks from meeting notes.

## New Features
- **LLM Extraction**: Uses Ollama (llama3.1) to intelligently find tasks.
- **Improved Frontend**: Added buttons for AI extraction and viewing saved notes.

## Setup
1. Install dependencies: `poetry install`
2. Start Ollama with `llama3.1:8b`
3. Run server: `poetry run uvicorn week2.app.main:app --reload`