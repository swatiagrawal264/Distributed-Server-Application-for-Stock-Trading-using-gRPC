#Import required libraries. 
import os
import sys
from flask import Flask, jsonify, request
import csv

import requests

#Initialize the Flask app
app = Flask(__name__)

#Initialize the order count and the filenames of the CSV files for logging and stock.
order_count = 0
order_log = "order_log"
stock_file = "Catalogue/stock.csv"
order_replicas = [(1,8000),(2,5001),(3,8002)]
ORDER_MICROSERVICE_URL = "http://127.0.0.1:"

script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
script_dir = os.path.split(os.path.split(script_path)[0])[0] #i.e. /path/to/dir/
stock_file_path = os.path.join(script_dir, stock_file)

# endpoint for placing an order
@app.route('/place_order', methods=['POST'])
def place_order():
    # Declare the order_count variable as global to be able to increment it inside the function
    global order_count
    # Get the JSON data from the POST request.
    order = request.get_json()
    # Extract the stock name, order type and quantity from the JSON data.
    stock_name = order['stock_name']
    order_type = order['order_type']
    quantity = int(order['quantity'])
    order_node = order['node']
    # Assign a transaction number to the order.
    transaction_number = order_count
    # Increment the order count.
    order_count += 1
    # Open the stock CSV file in read mode and loop through its rows.
    with open(stock_file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        for i in range(1, len(rows)):
            row = rows[i]
            # If the stock name matches a row in the CSV file.
            if row[0] == stock_name:
                stock_quantity = int(row[2])
                order_filename=getFileName(order_node)
                # If the order is a BUY and the quantity is less than or equal to the stock quantity.
                if order_type == 'BUY' and quantity <= stock_quantity:                   
                    # Subtract the quantity from the stock quantity and update the CSV file
                    row[2] = str(stock_quantity - quantity)
                    with open(stock_file_path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerows(rows)
                    # Log the transaction in the order log CSV file
                    with open(order_filename, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([transaction_number, stock_name, order_type, quantity])
                    # Return the transaction number as a JSON object.
                    return jsonify({'transaction_number': transaction_number})
                # If the order is a SELL.
                elif order_type == 'SELL':
                    # Add the quantity to the stock quantity and update the CSV file.
                    row[2] = str(stock_quantity + quantity)
                    with open(stock_file_path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerows(rows)
                    # Log the transaction in the order log CSV file.
                    with open(order_filename, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([transaction_number, stock_name, order_type, quantity])
                    # Return the transaction number as a JSON object.
                    for node in order_replicas:
                        if int(node[0])!=int(order_node):
                            order_data = {
                                            'stock_name': stock_name,
                                            'order_type': order_type,
                                            'quantity': quantity,
                                            'order_id': transaction_number,
                                            'node': order_node,
                                            'current_node': node[0]
                                        }
                            response = requests.post(ORDER_MICROSERVICE_URL +str(node[0])+ '/maintainData', json=order_data)
                    return True
# If the stock is not found or there is insufficient quantity, return an error message as a JSON object.
    return jsonify({'error': 'Stock not found or insufficient quantity'})

@app.route('/maintainData',methods=['POST'])
def maintainData():
    order=request.get_json()
    stock_name = order['stock_name']
    order_type = order['order_type']
    quantity = order['quantity']
    order_id = order['order_id']
    node = order['node']
    current_node=order['current_node']

    order_filename=getFileName(current_node)
    with open(order_filename, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([order_id, stock_name, order_type, quantity,node])
    return True
    
def getFileName(node):
    global order_log
    return order_log+str(node)+".csv"
        

if __name__ == '__main__':
    node=int(sys.argv[1])
    ORDER_PORT=int(order_replicas[node][1])
    print("listening on port", ORDER_PORT)
    app.run(debug=True, port=ORDER_PORT)
