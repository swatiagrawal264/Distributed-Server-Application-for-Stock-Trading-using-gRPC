import requests
import json

# Set server URL and port
server_url = "http://10.0.0.141:9999"

# Send Lookup request to look up the stocks 
def lookup_stock(stock_name):
    
    #Stock details url defined 
    url = f"{server_url}/stocks"
    data = {"stock_name": stock_name}
    response = requests.post(url, json=data)
    return response.json()

# Send buy and sell requests to the front end 
def send_request():
    action = input("Enter action (buy/sell): ")
    stock_name = input("Enter stock name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))
    #Specifying the actions to be committed
    if action == 'buy':
        endpoint = '/buy'
    elif action == 'sell':
        endpoint = '/sell'
    else:
        print('Invalid action')
        return
    
    #Buy and Sell urls defined
    url = f"{server_url}{endpoint}"
    data = {
        "action": action,
        "stock_name": stock_name,
        "quantity": quantity,
        "price": price
    }
    response = requests.post(url, json=data)
    print(response.json())
    
    
def main():
    stock_name = input("Enter stock name: ")
    print(lookup_stock(stock_name))

    while True:
        send_request()

if __name__ == '__main__':
    main()






