#Importing required modules
from flask import Flask, jsonify, request
import csv

#Creating a Flask instance
app = Flask(__name__)

# Initialize the stock list from CSV file
def load_stock():
    with open('stock.csv', 'r') as f:
        reader = csv.DictReader(f)
        stock = {}
        # Iterate over each row in CSV file and add it to stock dict
        for row in reader:
            stock[row['name']] = {
                'price': float(row['price']),
                'quantity': int(row['quantity'])
            }
        return stock

# Write the updated stock list to CSV file
def save_stock(stock):
    with open('stock.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'price', 'quantity'])
        writer.writeheader()
        for name, details in stock.items():
            writer.writerow({
                'name': name,
                'price': details['price'],
                'quantity': details['quantity']
            })

# Load the stock list from CSV file
stock = load_stock()

@app.route('/catalogue', methods=['GET'])
def get_catalogue():
# Return the stock list as JSON response
    return jsonify(stock)

@app.route('/catalogue/<string:name>', methods=['GET'])
def get_item(name):
    if name in stock:
# Return the details of the item as JSON response
        return jsonify(stock[name])
    else:
# Return error message as JSON response with 404 status code        
        return jsonify({'error': 'Item not found'}), 404

@app.route('/catalogue', methods=['POST'])
def add_item():
    name = request.json['name']
    if name in stock:
# Return error message as JSON response with 400 status code
        return jsonify({'error': 'Item already exists'}), 400
    else:
        price = request.json['price']
        quantity = request.json['quantity']
# Add new item to stock dict and save it to CSV file.
        stock[name] = {
            'price': price,
            'quantity': quantity
        }
        save_stock(stock)
        return jsonify({'message': 'Item added successfully'})

@app.route('/catalogue/<string:name>', methods=['PUT'])
def update_item(name):
    if name in stock:
        price = request.json['price']
        quantity = request.json['quantity']
# Update the details of existing item in stock dict and save it to CSV file
        stock[name] = {
            'price': price,
            'quantity': quantity
        }
        save_stock(stock)
        
# Return success message as JSON response
        return jsonify({'message': 'Item updated successfully'})
    else:
# Return error message as JSON response with 404 status code
        return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5002)

