import socket
import os


# taking inputs from environment variables to run locally and on docker
order_base_host = "localhost"
order_replicas = [(3,"8002"),(2,"5001"),(1,"8000")]

class OrderLeaderElection:
    def HealthCheck(host, p):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = server.connect_ex((host, p))
        server.close()
        if result == 0:
            return True
        else:
            return False
        
    def LeaderElection():
        leader=0
        for order_node in order_replicas:
            print(order_node[1])
            if OrderLeaderElection.HealthCheck(order_base_host,int(order_node[1])):
                    leader=order_node
                    print (f"leader:{leader}")
                    return leader
        return leader

    
 