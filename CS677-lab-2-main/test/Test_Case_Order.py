import json
import socket

HOST = 'localhost'
PORT = 8001

def send_request(sock):
    action = input("Enter action (buy/sell): ")
    stock_name = input("Enter stock name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))

    message = {'action': action, 'stock_name': stock_name, 'quantity': quantity, 'price': price}
    message_json = json.dumps(message)

    sock.sendall(message_json.encode('utf-8'))

    data = sock.recv(1024).decode('utf-8')
    response = json.loads(data)
    print(response)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print(f"[CONNECTED] Connected to server on {HOST}:{PORT}")

        while True:
            send_request(sock)

if __name__ == '__main__':
    main()


