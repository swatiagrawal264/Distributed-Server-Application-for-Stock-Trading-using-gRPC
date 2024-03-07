import socket
import threading

# Define the IP address and port number of the server
host = '127.0.0.1'
port = 10241


# Define the stock prices and volumes
MemeStocks = {
    'GameStart': {'price': 15.99, 'volume': 100},
    'FishCo': {'price': 10.99, 'volume': 200}
}

# Define the thread pool size
Threadpool_Size = 10

# Define the function to handle client requests
def handle_client(c, addr):
    print(f'Connected by {addr}')

    # Receive the stock name from the client and lookup the stock price
    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            break

        stock_name = data.strip()
        stock_data = MemeStocks.get(stock_name)

        if not stock_data:
            response = '-1'
        elif stock_data['volume'] == 0:
            response = '0'
        else: 
            response = f"{stock_data['price']}"

        # Send the stock price to the client
        c.sendall(str.encode(response))

    # Close the socket connection
    c.close()

# Define the thread pool
thread_pool = []

# Create the socket object and bind it to the IP address and port number
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

# Listen for incoming connections
s.listen(5)

# Accept incoming connections and handle them with the thread pool
while True:
    c, addr = s.accept()
    
    # lock acquired by client
    print("Connected to :", addr[0], ":", addr[1])

    if len(thread_pool) < Threadpool_Size:
        thread = threading.Thread(target=handle_client, args=(c, addr))
        thread_pool.append(thread)
        thread.start()
    else:
        # Wait for an available thread in the pool
        for thread in thread_pool:
            if not thread.is_alive():
                thread_pool.remove(thread)
                thread = threading.Thread(target=handle_client, args=(c, addr))
                thread_pool.append(thread)
                thread.start()
                break

# Close the socket connection
s.close()

