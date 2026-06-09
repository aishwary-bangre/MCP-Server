import base64
from email.message import EmailMessage
from auth import get_gmail_service

def create_email_draft(to: str, subject: str, body: str) -> str:
    """Creates a draft email in Gmail without sending it."""
    service = get_gmail_service()
    
    message = EmailMessage()
    
    # If the body contains HTML tags, we assume it's HTML
    if "<html>" in body.lower() or "<p>" in body.lower():
        message.add_alternative(body, subtype='html')
    else:
        message.set_content(body)
        
    message['To'] = to
    message['Subject'] = subject
    
    # Gmail API expects url-safe base64 encoding
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    create_message = {
        'message': {
            'raw': encoded_message
        }
    }
    
    draft = service.users().drafts().create(userId="me", body=create_message).execute()
    
    return f"Successfully created draft. Draft ID: {draft['id']}"
