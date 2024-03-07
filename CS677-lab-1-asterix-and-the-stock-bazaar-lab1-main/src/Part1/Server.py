import socket
import threading
import time

# Define the IP address and port number of the server, in thus case my machine IPv4 address
host = "10.0.0.141"
port = 8888

# Define the stock name, prices and volumes in the form of a dictionary
MemeStocks = {
    'GameStart': {'price': 15.99, 'volume': 100},
    'FishCo': {'price': 10.99, 'volume': 200}
   
}

# Counter for number of connected clients
num_clients = 0

# Define the thread pool size
Threadpool_Size = 2

# Define the function to handle client requests
def handle_client(c, addr):
    global num_clients
    num_clients += 1
    print(f"Connected to: {addr[0]}:{addr[1]} (Total clients: {num_clients})")
    
     
    # Receive the stock name from the client and lookup the stock price
    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            break
         #Timer Started to measure Latency period
        start_time = time.time()
        
        stock_name = data.strip().split()[1]
        stock_data = MemeStocks.get(stock_name)
        
        # Conditions defined to send an appropriate response to the client as per its request
        if not stock_data:
            response = '-1' #Incase name not found in the database
        elif stock_data['volume'] == 0:
            response = '0' #Incase name found in the database but volume is 0
        else: 
            response = f"{stock_data['price']}" #Incase name found and volume present

        # Send the stock price to the client
        c.sendall(str.encode(response))
        
        #Timer Ended to measure Latency period
        end_time = time.time()

        # Calculate and print the latency for this request
        latency = end_time - start_time
        print(f'Latency for request from {addr}: {latency:.6f}')

    # Close the socket connection
    c.close()
    #Calculate and print the number of clients connected to the server at a time
    num_clients -= 1
    print(f"Connection closed from: {addr[0]}:{addr[1]} (Total clients: {num_clients})")


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
     #Threadpool conditions specified
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
