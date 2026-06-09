# Google Workspace MCP Server

A FastAPI-based MCP-style server that exposes Google Docs and Gmail operations with a built-in Human-in-the-Loop (HITL) approval prompt for safety.

## Setup Instructions

1. **Google Cloud Console:**
   - Create a project.
   - Enable the **Google Docs API** and **Gmail API**.
   - Set up the OAuth consent screen.
   - Create OAuth 2.0 Client ID credentials (Desktop App).
   - Download the JSON and save it as `credentials.json` in this directory.

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server:**
   ```bash
   uvicorn server:app --reload
   ```

## Endpoints

- `POST /append_to_doc`
  - Body: `{"doc_id": "...", "content": "..."}`
- `POST /create_email_draft`
  - Body: `{"to": "...", "subject": "...", "body": "..."}`
