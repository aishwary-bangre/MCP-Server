# Walkthrough: Railway Deployment for Google Workspace MCP Server

The server has been successfully refactored and is fully ready to be deployed to Railway!

## What Was Changed

1. **Security & Port Binding (`server.py`)**
   - Removed the blocking `input()` prompt, which would have crashed on Railway's detached containers.
   - Added an `api_key` query parameter constraint to ensure endpoints remain secure.
   - Updated Uvicorn to listen on `0.0.0.0` and read the `$PORT` environment variable assigned dynamically by Railway.

2. **Cloud Credentials (`auth.py`)**
   - Added logic to seamlessly parse `GOOGLE_CREDENTIALS_JSON` and `GOOGLE_TOKEN_JSON` directly from the environment variables, ensuring you don't commit secrets to GitHub.

3. **Deployment Configuration (`Procfile`)**
   - Created a strict `Procfile` telling Railway exactly how to spin up the FastAPI application using Uvicorn.

## How to Deploy to Railway

Follow these exact steps to push this code live:

1. **Push to GitHub**
   Commit all files in the `groww-mcp-server` folder to a new private GitHub repository. **Make sure `credentials.json` and `token.json` are in your `.gitignore`!**

2. **Create Railway Project**
   - Go to [Railway.app](https://railway.app/).
   - Click **New Project** -> **Deploy from GitHub repo**.
   - Select the repository you just created.

3. **Add Environment Variables**
   Once the project is created, click on the service, go to the **Variables** tab, and add the following:
   
   - `MCP_API_KEY`: Create a strong secret password (e.g., `super-secret-groww-key-2026`). You will need to update the main pipeline clients to send this key!
   - `GOOGLE_CREDENTIALS_JSON`: Open your local `credentials.json` file, copy all the text, and paste it here.
   - `GOOGLE_TOKEN_JSON`: Open your local `token.json` file, copy all the text, and paste it here.

4. **Verify Deployment**
   Railway will automatically trigger a build and deploy. Once it goes green, Railway will provide you with a public URL (e.g., `https://groww-mcp-production.up.railway.app`).

> [!CAUTION]
> **Important Final Step**
> Once you get your Railway URL and your API Key, you must update `docs_client.py` and `gmail_client.py` in the main Groww pipeline to point to your new cloud URL instead of `127.0.0.1`, and append `?api_key=YOUR_SECRET` to the endpoint URL!
