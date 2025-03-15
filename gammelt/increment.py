# api/increment-endpoint.py
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

# This is the key class name that Vercel looks for
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get content length
        content_length = int(self.headers.get('Content-Length', 0))
        
        # Read and parse request body
        request_body = self.rfile.read(content_length).decode('utf-8')
        
        # Send response headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Process the request
        try:
            # Parse JSON data
            data = json.loads(request_body)
            
            # Get the number and increment it
            if 'number' in data:
                try:
                    number = int(data['number'])
                    result = {
                        "original": number,
                        "incremented": number + 1,
                        "timestamp": datetime.now().isoformat()
                    }
                except (ValueError, TypeError):
                    result = {
                        "error": "Invalid number format",
                        "message": "Please provide a valid number"
                    }
            else:
                result = {
                    "error": "Missing number",
                    "message": "Please provide a number in the request body"
                }
                
            # Send JSON response
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except json.JSONDecodeError:
            error_response = {
                "error": "Invalid JSON",
                "message": "Please provide valid JSON in the request body"
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
        except Exception as e:
            error_response = {
                "error": "Server Error",
                "message": str(e)
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def do_OPTIONS(self):
        # Handle CORS preflight request
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()