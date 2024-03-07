# Importing necessary packages and modules
from __future__ import print_function
import grpc
import time
from concurrent import futures
import part2gRPC_pb2_grpc as pb2_grpc
import part2gRPC_pb2 as pb2
import logging

# Defining the main function
def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    # Creating an insecure channel to connect with the gRPC server on 'localhost:50051'
    with grpc.insecure_channel('localhost:50051') as channel:
        
        # Creating a stub for the StockTrading service
        stub = pb2_grpc.StockTradingStub(channel)
        
        # Measure the time taken for a Lookup request
        start_time = time.monotonic()
        #Creating a Lookup request and passing the stock name.
        response = stub.Lookup(pb2.LookupRequest(stock_name = "FishCo"))
        end_time = time.monotonic()
        print(f"Lookup request took {end_time - start_time:.6f} seconds")
        print(response)
     
        
        # Measure the time taken for a Trade request
        start_time = time.monotonic()
        #Creating a Trade request and passing stock name, amount and is_buy
        response = stub.Trade(pb2.TradeRequest(stock_name = "FishCo", amount = 50000 , is_buy = True ))
        #end_time = time.monotonic()
        print(response)
        print(f"Trade request took {end_time - start_time:.6f} seconds")
        
        #Status for Update method
        response = stub.Update(pb2.UpdateRequest(stock_name= "GameStart", price= 15.99 ))
        print(response)
        
        
    


if __name__ == '__main__':
    logging.basicConfig()
    run()
    