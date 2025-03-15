import os  # Add this import
from http.server import HTTPServer
from hello import handler

# Define the server address
host = '0.0.0.0'
port = int(os.environ.get('PORT', 8000))  # Railway provides a PORT environment variable

# Create and start the server
server = HTTPServer((host, port), handler)
print(f"Server started on http://{host}:{port}")

try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
    print("Server stopped.")