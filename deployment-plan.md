# Railway Deployment Plan: Google Workspace MCP Server

This plan outlines the necessary architectural changes and steps to successfully deploy the FastAPI MCP Server to Railway.app.

## Goal Description
Transition the local MCP server into a production-ready state for deployment on Railway. This requires removing local terminal dependencies (like the HITL prompt), securing the endpoints, and configuring Google Cloud to accept cloud-based OAuth redirects.

## User Review Required

> [!WARNING]
> **The Human-in-the-Loop (HITL) Prompt**
> Railway runs your server in the cloud with no interactive terminal. The `Approve? (y/n)` terminal prompt will cause the server to freeze permanently on Railway.
> **Decision needed:** Should we completely remove the `require_approval` step, or replace it with a simple API Key verification (e.g., passing a secret token in the request headers) to ensure safety?

## Open Questions

> [!IMPORTANT]
> **Handling Google Credentials**
> We cannot commit `credentials.json` and `token.json` to GitHub. The best practice for Railway is to store the contents of these files as Railway Environment Variables (e.g., `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_TOKEN_JSON`). Does this approach work for you?

## Proposed Changes

### `groww-mcp-server/`

#### [MODIFY] [server.py](file:///d:/cursor%20projects/groww-mcp-server/server.py)
- **Remove HITL:** Remove the blocking `input()` prompt.
- **Port Binding:** Update the uvicorn start command to bind to `0.0.0.0` and read the `PORT` environment variable injected by Railway.
- **API Key Security (Optional):** Add a simple FastAPI middleware to check for an `X-API-KEY` header to keep the endpoints secure since the HITL prompt is gone.

#### [MODIFY] [auth.py](file:///d:/cursor%20projects/groww-mcp-server/auth.py)
- Update credential loading logic to check for `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_TOKEN_JSON` environment variables first before falling back to looking for local `.json` files on disk.

#### [NEW] [Procfile](file:///d:/cursor%20projects/groww-mcp-server/Procfile)
- Create a standard Procfile to explicitly tell Railway how to start the app:
  `web: uvicorn server:app --host 0.0.0.0 --port $PORT`

## Verification Plan

### Manual Verification
1. Create a Railway project connected to the GitHub repo.
2. Add the environment variables (`GOOGLE_CREDENTIALS_JSON`, `GOOGLE_TOKEN_JSON`, and `API_KEY`).
3. Deploy the application.
4. Send a Postman/Curl request to the live Railway URL to verify it successfully appends to Google Docs.
