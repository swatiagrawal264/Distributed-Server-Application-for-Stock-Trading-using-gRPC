from http.server import BaseHTTPRequestHandler, HTTPServer


HOST = "127.0.0.1"
PORT = 9999
class myHTTPRH(BaseHTTPRequestHandler):
    
   """ def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        """
   def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        self.wfile.write(bytes("<html><body><h1>data: {name: GameStart,price: 15.99,quantity: 100}</h1></body></html>","utf-8"))
  
   def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('{"name": "GameStart","quantity": 1,"type": "sell"}'  "utf-8"))
        
server = HTTPServer((HOST, PORT), myHTTPRH)
print("Server running")
server.serve_forever()
server.server_close()
print("Server Stopped")  