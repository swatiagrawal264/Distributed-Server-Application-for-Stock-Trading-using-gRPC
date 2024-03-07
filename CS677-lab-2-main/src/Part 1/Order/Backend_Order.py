import socket
import threading
import csv
import json
from rwlock import RWLock  # import the read-write lock

# Host and Port of this microservice are decalred
HOST = 'localhost'
PORT = 8002

stock = {}
catalogue_lock = RWLock()  # create the read-write lock object

# Loading the stock_catalogue.csv to retrieve the desired information
def load_stock_catalogue():
    global stock
    with open('stock_catalogue.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            with catalogue_lock.reader_lock:
                 stock[row[0]] = {'quantity': int(row[1]), 'price': float(row[2])}

# Here we are updating the stock_catalogue.csv as the customer buys or sells the stocks
def save_stock_catalogue():
    global stock
    with open('stock_catalogue.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for stock_name, stock_info in stock.items():
            writer.writerow([stock_name, stock_info['quantity'], stock_info['price']])

# Here we are updating the details of each transaction 
def save_trade_data(trade_info):
    with open('trades_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([trade_info['stock'], trade_info['quantity'], trade_info['price'], trade_info['status'], trade_info['message']])

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
        
        # Acquire write lock before updating catalogue
        catalogue_lock.acquire_write()
        
        try: 

        # This code snippet has been designed to handle the buy requests of the client
        if action == "buy":
            quantity = data['quantity']
            price = data['price']
            
                # Here the information provided by the client is being processed 
                if stock_name in stock and quantity <= stock[stock_name]['quantity']:
                    stock[stock_name]['quantity'] -= quantity
                    stock[stock_name]['price'] = price
                    
                    # The trade is being declared a success if given trade is in stock and the given quantity is available
                    trade_info = {'stock': stock_name, 'quantity': quantity, 'price': price, 'status': 'success', 'message': 'Buy successful'}
                else:
                    
                    # The trade is being declared a failure if given quantity is not in the stock
                    trade_info = {'stock': stock_name, 'quantity': quantity, 'price': price, 'status': 'failure', 'message': 'Buy unsuccessful'}
                
                # The trade information is being saved
                save_trade_data(trade_info)
                save_stock_catalogue()
                conn.send(json.dumps(trade_info).encode('utf-8'))
                
            # Here the client's request to sell their stocks is being processed
            elif action == "sell":
                quantity = data['quantity']
                price = data['price']
                
                # Acquire write lock to modify the stock catalogue
                catalogue_lock.acquire_write()

                try:
                
                # Here the information provided by the client is being processed
                if stock_name in stock:
                    stock[stock_name]['quantity'] += quantity
                    stock[stock_name]['price'] = price
                    
                    # The trade is being declared a success if given trade is in stock and the given quantity is available
                    trade_info = {'stock': stock_name, 'quantity': quantity, 'price': price, 'status': 'success', 'message': 'Sell successful'}
                else:
                    
                    # The trade is being declared a failure if given stock is not in the list
                    trade_info = {'stock': stock_name, 'quantity': quantity, 'price': price, 'status': 'failure', 'message': 'Sell unsuccessful'}
                
                #Trade information is being saved
                save_trade_data(trade_info)
                save_stock_catalogue()
                conn.send(json.dumps(trade_info).encode('utf-8'))
                
                finally:
                    # Release the write lock
                    catalogue_lock.release_write()

        finally:
            # Release the read lock
            catalogue_lock.release_read()
                
                
        #Connection Closed
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
