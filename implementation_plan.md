# Implementation Plan: Google Workspace MCP Server

This plan outlines the architecture for a FastAPI-based MCP-style server that integrates with Google Docs and Gmail, built exactly to the specified requirements.

## Goal Description
Build a Python-based server using FastAPI that securely wraps the Google Docs API and Gmail API. It will expose HTTP POST endpoints for external clients to append content to Docs and create Gmail drafts. Crucially, it features a Human-in-the-Loop (HITL) approval prompt in the terminal before executing any action.

## Proposed Changes

### `google-mcp-server/` (Project Structure)
The core repository structure for the server.

#### [NEW] `server.py`
- Uses `FastAPI` + `uvicorn`.
- Exposes two endpoints:
  - `POST /append_to_doc`: accepts `doc_id` and `content`.
  - `POST /create_email_draft`: accepts `to`, `subject`, and `body`.
- **Security/Safety Feature:** Before executing, prints the action name and payload in the terminal and asks `Approve? (y/n)`. Only proceeds if the user types `y`.

#### [NEW] `auth.py`
- Handles Google OAuth 2.0 flow.
- Scopes: `https://www.googleapis.com/auth/documents` and `https://www.googleapis.com/auth/gmail.compose`.
- Loads from `credentials.json` (not committed).
- Saves/loads access tokens via `token.json` (not committed) to skip browser login after the first run.

#### [NEW] `docs_tool.py`
- Function: `append_to_doc(doc_id: str, content: str)`.
- Connects to Google Docs API to append text/markdown to the end of the specified document.

#### [NEW] `gmail_tool.py`
- Function: `create_email_draft(to: str, subject: str, body: str)`.
- Connects to Gmail API to create a draft email (does NOT send automatically) for safety and review.

#### [NEW] `requirements.txt`
- Dependencies: `fastapi`, `uvicorn`, `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`.

#### [NEW] `README.md`
- Detailed setup instructions for creating the Google Cloud project, downloading `credentials.json`, and running the uvicorn server.

## Verification Plan

### Automated/Local Testing
1. Start the server using `uvicorn server:app --reload`.
2. Send a curl/Postman request to `/append_to_doc`. Verify the terminal halts and asks `Approve? (y/n)`.
3. Type `y` and verify the Google Doc updates.
4. Send a request to `/create_email_draft`, approve it, and verify the draft appears in the Gmail account.
