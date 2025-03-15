from http.server import BaseHTTPRequestHandler
import json
from increment import process_increment


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get content length from headers
        content_length = int(self.headers['Content-Length'])
        
        # Read request body
        post_data = self.rfile.read(content_length)
        
        try:
            # Parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            
            # Process the data using our core logic
            result, status_code = process_increment(data)
            
            # Set response headers
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            self.end_headers()
            
            # Send response
            self.wfile.write(json.dumps(result).encode('utf-8'))
                
        except json.JSONDecodeError:
            # Handle invalid JSON
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error = {
                "error": "Invalid JSON",
                "message": "Please provide valid JSON in the request body"
            }
            self.wfile.write(json.dumps(error).encode('utf-8'))
    
    def do_OPTIONS(self):
        # Handle preflight CORS requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.end_headers()