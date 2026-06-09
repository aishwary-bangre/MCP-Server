# Render Deployment Plan: Google Workspace MCP Server

Since Railway's free tier is maxed out, we will pivot to deploying the MCP Server on [Render.com](https://render.com/), which offers an excellent free tier perfectly suited for FastAPI apps.

## Goal Description
Modify the repository configuration to support automated, 1-click Blueprint deployments on Render.

## Proposed Changes

### `groww-mcp-server/`

#### [NEW] [render.yaml](file:///d:/cursor%20projects/groww-mcp-server/render.yaml)
- Create Render's "Infrastructure as Code" file.
- Define the Web Service (Python environment).
- Set `buildCommand: pip install -r requirements.txt`.
- Set `startCommand: uvicorn server:app --host 0.0.0.0 --port $PORT`.
- Define the required environment variables (`MCP_API_KEY`, `GOOGLE_CREDENTIALS_JSON`, `GOOGLE_TOKEN_JSON`) so Render prompts you for them during setup.

#### [DELETE] [Procfile](file:///d:/cursor%20projects/groww-mcp-server/Procfile)
- Remove the Railway-specific configuration file to avoid clutter.

## Verification Plan

### Manual Verification
1. Push these changes to GitHub.
2. Go to Render.com -> Click "New" -> "Blueprint".
3. Connect the GitHub repository.
4. Render will automatically read the `render.yaml` file, prompt you to paste your 3 environment variables, and build the server.
5. Verify the live Render URL accepts HTTP requests.
