import socket
import json

HOST = 'localhost'
PORT = 8001

def lookup_stock(stock_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = {'action': 'lookup', 'stock_name': stock_name}
        s.send(json.dumps(message).encode('utf-8'))
        response = s.recv(1024)
        response = json.loads(response.decode('utf-8'))
        return response

    

if __name__ == '__main__':
    stock_name = input("Enter stock name: ")
    print(lookup_stock(stock_name))


