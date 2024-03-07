import socket
import threading
import csv
import json

# Host and Port of this microservice declared 
HOST = 'localhost'
PORT = 8001

stock = {}

# Loading the stock_catalogue.csv to retrieve the desired information
def load_stock_catalogue():
    global stock
    with open('stock_catalogue.csv', 'r') as f:
        #Information being read from the csv file
        reader = csv.reader(f)
        for row in reader:
            #The first column is stock name, second is quantity and third is price
            stock[row[0]] = {'quantity': int(row[1]), 'price': float(row[2])}

# Finction defined to hangle incoming client requests through the front end microservice
def handle_client(conn, addr):
    #Print client address when connected
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        data = conn.recv(1024)
        if not data:
            
            #Print client disconnected
            print(f"[DISCONNECTED] {addr} disconnected.")
            break
        #data being received is loaded in json format
        data = data.decode('utf-8')
        data = json.loads(data)
        action = data['action']
        stock_name = data['stock_name']
        
        #Lookup operation is being performed to look up the details of the stock
        if action == "lookup":
            if stock_name in stock:
                #stock details being read if the stock is available in the catalogue
                message = {'status': 'success', 'data': {'quantity': stock[stock_name]['quantity'], 'price': stock[stock_name]['price']}}
            else:
                #if the stock in unavailable the name not found message sent to client
                message = {'status': 'failure', 'message': f"Stock: {stock_name} not found in catalogue."}
            conn.send(json.dumps(message).encode('utf-8'))
    
    #Connection to the front end is closed.
    conn.close()

def main():
    load_stock_catalogue()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    s.listen()

    while True:
        #Threading implemented
        conn, addr = s.accept()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
    #socket connection is closed
    s.close()

if __name__ == '__main__':
    main()
