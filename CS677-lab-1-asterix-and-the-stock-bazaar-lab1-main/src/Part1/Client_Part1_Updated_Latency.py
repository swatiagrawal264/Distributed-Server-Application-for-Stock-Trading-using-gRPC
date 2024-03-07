import socket
import random
import time

def main():
    # local host IP '10.0.0.141'
    host = "10.0.0.141"
    # Define the port on which you want to connect
    port = 8888

    # Define the stock names and messages to send to the server 
    # added 3 dummy names as well to automate the process and get -1 as response
    stock_names = ['GameStart', 'FishCo', 'Google', 'Amazon', 'Apple']
    messages = [f"lookup {name}" for name in stock_names]
   
    while True:
        # Choose a random message to send
        message = random.choice(messages)

        if message.lower() == "exit":
            break
        # Create the socket object and bind it to the IP address and port number
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        s.connect((host, port))

        # Send the message to the server
        start_time = time.time()
        s.send(message.encode("ascii"))

        # Receive the response from the server
        response = s.recv(1024).decode("ascii")
        end_time = time.time()

        # Print the response and the time latency
        if response == '-1':
            print(f"Stock {message.split()[1]} not found : -1 ")
        elif response == '0':
            print(f"Stock {message.split()[1]} is out of stock: 0 ")
        else:
            print(f"The price of {message.split()[1]} is {response}. Latency: {end_time - start_time:.6f} seconds")

        # Close the connection
        s.close()

if __name__ == "__main__":
    main()
