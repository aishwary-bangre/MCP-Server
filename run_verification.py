import subprocess
import time
import requests
import threading
import sys

def run_server():
    # Start the FastAPI server using uvicorn directly
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "server:app", "--host", "127.0.0.1", "--port", "8000"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd="."
    )
    return server_process

def test_append_to_doc():
    url = "http://127.0.0.1:8000/append_to_doc"
    payload = {
        "doc_id": "1yDummyDocID_PleaseIgnore-1234567890",
        "content": "## Automated Test Entry\nThis is a verification test."
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"\n[CLIENT] append_to_doc Response: {response.status_code}")
        print(f"[CLIENT] Body: {response.text}")
    except Exception as e:
        print(f"\n[CLIENT] Request failed: {e}")

if __name__ == "__main__":
    print("Starting server...")
    server = run_server()
    
    # Wait for server to boot
    time.sleep(3)
    
    print("Sending request in background thread...")
    client_thread = threading.Thread(target=test_append_to_doc)
    client_thread.start()
    
    # Wait a second for the request to reach the server
    time.sleep(1)
    
    print("Sending 'y' to server stdin to approve the action...")
    server.stdin.write("y\n")
    server.stdin.flush()
    
    # Wait for the client thread to finish receiving the response
    client_thread.join()
    
    print("Terminating server...")
    server.terminate()
    print("Verification complete.")
