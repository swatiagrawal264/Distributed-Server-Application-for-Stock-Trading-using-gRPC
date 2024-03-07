# Importing necessary packages and modules
import grpc
import threading
import logging
from concurrent import futures
import time
import part2gRPC_pb2_grpc as pb2_grpc
import part2gRPC_pb2 as pb2

#Created a class named StockTradingService
class StockTradingService(pb2_grpc.StockTradingServicer):
    
    #Initialize the stock catalog with four stocks.
    def __init__(self):
        self.stock_catalog = {'GameStart': {'price': 15.99, 'volume': 1300},
                              'FishCo': {'price': 11.25, 'volume': 150},
                              'BoarCo': {'price': 39.98, 'volume': 370},
                              'MenhirCo': {'price': 27.99, 'volume': 450}}
        #Setting maximum trading volume for each stock.
        self.max_volume = {
            'GameStart': 1000,
            'FishCo': 2000,
            'BoarCo': 3000,
            'MenhirCo': 4000,
        }
        
        self.trading_suspended = False
        
        #Creating a lock
        self.lock = threading.Lock()
        
    #Lookup function to check stock availability.    
    def Lookup(self, request,context):
        stock_name = request.stock_name
        #with self.lock:
        if stock_name in self.stock_catalog:
            response= pb2.LookupResponse(price=self.stock_catalog[stock_name]["price"], volume= self.stock_catalog[stock_name]["volume"])
            return response
            
        else:
            return pb2.LookupResponse(price=-1, volume=0)
        
     # Trade function to buy and sell stocks   
    def Trade(self, request, context):
        stock_name = request.stock_name
        amount = request.amount
        if self.stock_catalog[stock_name]["volume"] > (self.max_volume[stock_name]):
            self.trading_suspended = True
        buy = request.is_buy
        if self.trading_suspended is not True:
            if stock_name not in self.stock_catalog:
                return pb2.TradeResponse(status = -1)
            else:
                 if buy:
                     self.stock_catalog[stock_name]["volume"] += amount
                     return pb2.TradeResponse(status = 1)
                 else:
                     self.stock_catalog[stock_name]["volume"] -= amount
                     return pb2.TradeResponse(status = 1)
        else:
            return pb2.TradeResponse(status = 0)
        
    #Update function to modify stock prices.
    def Update(self, request, context):
          
          stock_name = request.stock_name
          new_price = request.price
          #with self.lock:
          if stock_name in self.stock_catalog:
              self.stock_catalog[stock_name]["price"] = new_price
              return pb2.UpdateResponse(status = 1)
          elif new_price<0:
              return pb2.UpdateResponse(status = -2)
          else:
              return pb2.UpdateResponse(status = -1)
          
# Send a request and measure the time taken
#Start the server  
def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_StockTradingServicer_to_server(StockTradingService(), server)
        server.add_insecure_port('[::]:50051')
        start_time = time.monotonic() # measure the start time
        server.start()
        end_time = time.monotonic() # measure the end time
        #Time taken by server to start
        print(f"Server started in {end_time - start_time:.6f} seconds")
       # print("Server started")
        server.wait_for_termination()
        
# Start a timer for one day
        seconds_per_day = 60 * 60 * 24
        end_time = time.time() + seconds_per_day

    # Keep the server running until the timer expires
        try:
         while True:
            time.sleep(seconds_per_day)
        except KeyboardInterrupt:
         server.stop(0)
        


if __name__ == '__main__':
    logging.basicConfig()
    serve()
    