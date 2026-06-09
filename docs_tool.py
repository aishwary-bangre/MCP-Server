from auth import get_docs_service

def append_to_doc(doc_id: str, content: str) -> str:
    """Appends text to the end of a Google Doc."""
    service = get_docs_service()
    
    # We use endOfSegmentLocation to append directly to the end of the main body
    requests = [
        {
            'insertText': {
                'endOfSegmentLocation': {
                    'segmentId': ''  # empty string means the main body
                },
                'text': "\n" + content + "\n"
            }
        }
    ]
    
    result = service.documents().batchUpdate(
        documentId=doc_id, body={'requests': requests}
    ).execute()
    
    return f"Successfully appended content to document {doc_id}."
