import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/gmail.compose'
]

import json
from google.oauth2.credentials import Credentials

def get_credentials():
    """Gets valid user credentials from storage or initiates OAuth flow."""
    creds = None
    
    # Railway Environment Variables Support
    env_token = os.environ.get('GOOGLE_TOKEN_JSON')
    env_creds = os.environ.get('GOOGLE_CREDENTIALS_JSON')

    token_path = os.path.join(os.path.dirname(__file__), 'token.json')
    creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')

    # 1. Try loading from Env Var first (Railway)
    if env_token:
        try:
            token_dict = json.loads(env_token)
            creds = Credentials.from_authorized_user_info(token_dict, SCOPES)
        except Exception as e:
            print(f"Failed to load token from Env Var: {e}")
            
    # 2. Try loading from file (Local Dev)
    elif os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except ValueError:
            pass

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # We need client secrets. Try env var first.
            if env_creds:
                creds_dict = json.loads(env_creds)
                flow = InstalledAppFlow.from_client_config(creds_dict, SCOPES)
            elif os.path.exists(creds_path):
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            else:
                raise FileNotFoundError(f"Missing {creds_path} or GOOGLE_CREDENTIALS_JSON environment variable.")
                
            # Note: run_local_server will fail on Railway. Ensure token.json is generated locally first!
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next local run
        try:
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        except Exception:
            pass # Fails silently on readonly filesystems

    return creds

def get_docs_service():
    """Builds and returns the Google Docs API service."""
    creds = get_credentials()
    return build('docs', 'v1', credentials=creds)

def get_gmail_service():
    """Builds and returns the Gmail API service."""
    creds = get_credentials()
    return build('gmail', 'v1', credentials=creds)
