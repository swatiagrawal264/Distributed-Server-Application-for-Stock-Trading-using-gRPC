import json
import socket
from http.server import BaseHTTPRequestHandler,HTTPServer
import threading

# Define constants
TRADES_HOST = 'localhost'
TRADES_PORT = 8002
STOCKS_HOST = 'localhost'
STOCKS_PORT = 8001
HOST = '10.0.0.141'
PORT = 9999


class myHTTPRH(BaseHTTPRequestHandler):
    
    # Define function to handle GET requests
    def do_GET(self):       
        if self.path == '/stocks':
            # Connect to stocks microservice
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((STOCKS_HOST, STOCKS_PORT))
                # Send request for stocks data
                s.send(b'get_stocks')
                # Receive response from stocks microservice
                data = s.recv(1024)
            # Parse response data as JSON
            stocks_data = json.loads(data.decode())
            # Set response headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Send stocks data as JSON response
            self.wfile.write(json.dumps(stocks_data).encode())
            
        else:
            # Send error response for invalid path
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')
            
    # Define function to handle POST requests
    def do_POST(self):
        if self.path == '/buy':
            # Parse request data as JSON
            content_length = int(self.headers['Content-Length'])
            request_data = json.loads(self.rfile.read(content_length))
            # Connect to trades microservice
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((TRADES_HOST, TRADES_PORT))
                # Send request to buy stock
                request = f"{request_data['user_id']},{request_data['stock_name']},{request_data['quantity']},{request_data['price']}"
                
                s.send(request.encode())
                # Receive response from trades microservice
                response = s.recv(1024)
            # Set response headers
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            # Send response from trades microservice as plain text response
            self.wfile.write(response)
            
        elif self.path == '/sell':
            # Parse request data as JSON
            content_length = int(self.headers['Content-Length'])
            request_data = json.loads(self.rfile.read(content_length))
            
            # Retrieve data from request
            user_id = request_data.get('user_id')
            stock_name = request_data.get('stock_name')
            quantity = request_data.get('quantity')
            price = request_data.get('price')
            
            
            # Connect to trades microservice
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                 s.connect((TRADES_HOST, TRADES_PORT))
                 # Send request to sell stock
                 request = f"{user_id},{stock_name},{quantity},{price}"
                 
                 s.send(request.encode())

            # Receive response from trades microservice
            response = s.recv(1024).decode()

            # Return response to client
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': response}).encode())
            
server = HTTPServer((HOST,PORT),myHTTPRH)
print("Server Now running...")
server.serve_forever()
server.server_close()
print("Server Stopped!")
