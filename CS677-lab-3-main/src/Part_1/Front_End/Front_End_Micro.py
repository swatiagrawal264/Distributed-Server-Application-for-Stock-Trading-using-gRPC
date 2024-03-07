#Import required libraries.
from flask import Flask, request, jsonify
import requests
from Replication import OrderLeaderElection

# Create a Flask app instance
app = Flask(__name__)

# Define the URLs for the microservices and transaction number.
CATALOGUE_MICROSERVICE_URL = "http://127.0.0.1:5002"
ORDER_MICROSERVICE_URL = "http://127.0.0.1:"
TRANSACTION_NUMBER = 0

# Define the endpoint to retrieve the entire catalogue.
@app.route('/catalogue', methods=['GET'])
def get_catalogue():
    response = requests.get(CATALOGUE_MICROSERVICE_URL + '/catalogue')
    return response.content, response.status_code

# Define the endpoint to retrieve an item from the catalogue.
@app.route('/catalogue/<string:name>', methods=['GET'])
def get_item(name):
    if (name in cache):
        print(f"{name}Found in cache")
        response=cache[name]
        return response
    else:
# Make a GET request to the Catalogue Microservice to retrieve the item with the given name.
        response = requests.get(CATALOGUE_MICROSERVICE_URL + '/catalogue/' + name)
    
# If the item is not found, return a 404 error response.
        if response.status_code != 200:
            return jsonify({'error': 'Item not found.'}), 404
        else:
            cache[name]=response.content.decode()
            print(f"{name} Added to cache")
# If the item is found, return the item details and a 200 success response.
    return response.content, response.status_code
    

# Define the endpoint to add an item to the catalogue.
@app.route('/catalogue', methods=['POST'])
def add_item():
    
# Retrieve the item data from the request body.
    data = request.get_json()
    name = data['name']
    price = data['price']
    quantity = data['quantity']

# Create a dictionary of the item data.
    item_data = {
        'name': name,
        'price': price,
        'quantity': quantity
    }

# Make a request to the Catalogue Microservice to add an item.
    response = requests.post(CATALOGUE_MICROSERVICE_URL + '/catalogue', json=item_data)
# If the item is not added successfully, return a 500 error response.
    if response.status_code != 200:
        return jsonify({'error': 'Failed to add item.'}), 500

# If the item is added successfully, return a success message and a 200 success response.
    return jsonify({'message': 'Item added successfully.'}), 200

# Define the endpoint to update an item in the catalogue.
@app.route('/catalogue/<string:name>', methods=['PUT'])

# Retrieve the item data from the request body
def update_item(name):
    data = request.get_json()
    price = data['price']
    quantity = data['quantity']

# Create a dictionary of the updated item data.
    item_data = {
        'price': price,
        'quantity': quantity
    }

# Make a request to the Catalogue Microservice to update an item.
    response = requests.put(CATALOGUE_MICROSERVICE_URL + '/catalogue/' + name, json=item_data)

# If the item is not added successfully, return a 500 error response.
    if response.status_code != 200:
        return jsonify({'error': 'Failed to update item.'}), 500
    if (name in cache):
        del cache[name]
        print(f"Removed {name} from cache")
    
# If the item is added successfully, return a success message and a 200 success response.
    return jsonify({'message': 'Item updated successfully.'}), 200


@app.route('/place_order', methods=['POST'])
def place_order():
    value=getLeaderPort()
    print(value)
    print(type(value))
    order_port=value[1]
    order_node=value[0]
    data = request.get_json()
    stock_name = data['stock_name']
    order_type = data['order_type']
    quantity = data['quantity']

# Create a dictionary with the order data.
    order_data = {
        'stock_name': stock_name,
        'order_type': order_type,
        'quantity': quantity,
        'node': order_node
    }

# Make a POST request to the Order Microservice with the order data as JSON.
    response = requests.post(ORDER_MICROSERVICE_URL +str(order_port)+ '/place_order', json=order_data)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to place order.'}), 500

# Get the transaction number and increment the global transaction counter.
    global TRANSACTION_NUMBER
    transaction_number = TRANSACTION_NUMBER
    TRANSACTION_NUMBER += 1

# Return a JSON response with the transaction number and a 200 status code.
    return jsonify({'transaction_number': transaction_number}), 200


def getLeaderPort():
    leader=OrderLeaderElection.LeaderElection()
    return leader


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    cache={}
