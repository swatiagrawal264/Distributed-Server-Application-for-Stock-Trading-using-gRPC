import socket
import threading
import csv
import json

HOST = 'localhost'
PORT = 8001

stock = {}

def load_stock_catalogue():
    global stock
    with open('stock_catalogue.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            stock[row[0]] = {'quantity': int(row[1]), 'price': float(row[2])}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        data = conn.recv(1024)
        if not data:
            print(f"[DISCONNECTED] {addr} disconnected.")
            break

        data = data.decode('utf-8')
        data = json.loads(data)
        action = data['action']
        stock_name = data['stock_name']

        if action == "lookup":
            if stock_name in stock:
                message = {'status': 'success', 'data': {'quantity': stock[stock_name]['quantity'], 'price': stock[stock_name]['price']}}
            else:
                message = {'status': 'failure', 'message': f"Stock: {stock_name} not found in catalogue."}
            conn.send(json.dumps(message).encode('utf-8'))

    conn.close()

def main():
    load_stock_catalogue()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    s.listen()

    while True:
        conn, addr = s.accept()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

    s.close()

if __name__ == '__main__':
    main()
