from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys

from docs_tool import append_to_doc
from gmail_tool import create_email_draft

app = FastAPI(title="Google Workspace MCP Server")

class DocRequest(BaseModel):
    doc_id: str
    content: str

class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str

import os

API_KEY = os.environ.get("MCP_API_KEY", "dev-secret-key") # Default for local testing

def require_approval(action_name: str, payload: dict, api_key: str):
    """
    Railway doesn't support interactive terminals. 
    We replace the terminal HITL prompt with a strict API Key check.
    """
    if not api_key or api_key != API_KEY:
        print(f"X Action '{action_name}' rejected: Invalid API Key.")
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
    print(f"OK Action '{action_name}' approved via valid API Key. Executing...\n")

@app.post("/append_to_doc")
def handle_append_to_doc(req: DocRequest, api_key: str = None):
    require_approval("APPEND_TO_DOC", req.model_dump(), api_key)
    
    try:
        result = append_to_doc(req.doc_id, req.content)
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create_email_draft")
def handle_create_email_draft(req: EmailRequest, api_key: str = None):
    require_approval("CREATE_EMAIL_DRAFT", req.model_dump(), api_key)
    
    try:
        result = create_email_draft(req.to, req.subject, req.body)
        return {"status": "success", "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
