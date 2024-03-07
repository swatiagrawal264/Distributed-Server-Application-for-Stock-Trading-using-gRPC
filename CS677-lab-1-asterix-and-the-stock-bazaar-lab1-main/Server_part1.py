# import socket programming library
import socket

# import threadpool module
from concurrent.futures import ThreadPoolExecutor


# thread function
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print("Bye")
            break

        # reverse the given string from client
        data = data[::-1]

        # send back reversed string to client
        c.send(data)

    # connection closed
    c.close()