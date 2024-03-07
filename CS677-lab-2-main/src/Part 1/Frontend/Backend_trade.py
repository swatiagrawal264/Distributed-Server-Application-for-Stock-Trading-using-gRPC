import csv
import socket
import threading
from concurrent.futures import ThreadPoolExecutor

# Define constants
HOST = 'localhost'
PORT = 8002
THREAD_POOL_SIZE = 10
TRADE_DATA_FILENAME = 'trades.csv'
STOCK_CATALOG_FILENAME = 'stock_catalogue.csv'

# Create thread pool
pool = ThreadPoolExecutor(THREAD_POOL_SIZE)

# Define function to handle incoming client requests
def handle_client(conn, addr):
    # Receive message from client
    data = conn.recv(1024)
    message = data.decode()

    # Split message into components
    components = message.split(',')

    # Extract trade details from message
    user_id = components[0]
    stock_name = components[1]
    quantity = int(components[2])
    price = float(components[3])

    # Read stock catalog from file
    with open(STOCK_CATALOG_FILENAME, 'r') as f:
        reader = csv.reader(f)
        stock_catalog = list(reader)

    # Find stock in catalog
    stock_found = False
    for stock in stock_catalog:
        if stock[0] == stock_name:
            stock_found = True
            available_quantity = int(stock[1])
            break

    # If stock not found, send error message
    if not stock_found:
        response = f"Trade failed: {stock_name} not found in stock catalog"
        conn.send(response.encode())
        conn.close()
        return

    # If stock found but not available, send error message
    if quantity > available_quantity:
        response = f"Trade failed: {stock_name} only has {available_quantity} units available"
        conn.send(response.encode())
        conn.close()
        return

    # Calculate total cost of trade
    total_cost = quantity * price

    # Read trade data from file
    with open(TRADE_DATA_FILENAME, 'r') as f:
        reader = csv.reader(f)
        trade_data = list(reader)

    # Find highest trade ID
    trade_id = int(trade_data[-1][0]) + 1

    # Add trade to trade data
    trade_data.append([trade_id, user_id, stock_name, quantity, price, total_cost])

    # Write updated trade data to file
    with open(TRADE_DATA_FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(trade_data)

    # Update stock catalog
    for stock in stock_catalog:
        if stock[0] == stock_name:
            stock[1] = str(int(stock[1]) - quantity)
            break

    # Write updated stock catalog to file
    with open(STOCK_CATALOG_FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(stock_catalog)

    # Send success message to client
    response = f"Trade successful: {quantity} units of {stock_name} purchased for {total_cost:.2f} USD"
    conn.send(response.encode())
    conn.close()

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to host and port
s.bind((HOST, PORT))

# Listen for incoming connections
s.listen()

# Handle incoming connections
while True:
    conn, addr = s.accept()
    print(f"New connection from {addr}")
    pool.submit(handle_client, conn, addr)
