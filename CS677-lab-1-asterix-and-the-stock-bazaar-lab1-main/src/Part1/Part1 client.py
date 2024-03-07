# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:19:49 2023

@author: Medha
"""
import socket


def main():
    # local host
    #host = socket.gethostname()
    host = "127.0.0.1"
    # Define the port on which you want to connect
    port = 10241



    # message you send to server
    while True:
        
       message = input("please enter the name of the stock, type exit to stop\n")

       if message.lower() == "exit":
           break

       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to server
       s.connect((host, port))

        # message sent to server
       s.send(message.encode("ascii"))

        # message received from server
       data = s.recv(1024)

        # print the received message
        # here it would be a reverse of sent message
       print("Server replied: {}".format(str(data.decode("ascii"))))

        # close the connection
       s.close()


if __name__ == "__main__":
    main()
