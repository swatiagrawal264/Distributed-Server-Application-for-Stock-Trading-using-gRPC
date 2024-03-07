import requests

# URL of the front-end service
FRONT_END_URL = "http://127.0.0.1:5000"

# Displays the menu options
def print_menu():
    print("1. View catalogue")
    print("2. Place order")
    print("3. Quit")

# Sends a GET request to the front-end service to retrieve the catalogue data and displays it.
def view_catalogue():
    response = requests.get(FRONT_END_URL + '/catalogue')
    if response.status_code == 200:
        catalogue = response.json()
        for item_name, item_details in catalogue.items():
            print(f"{item_name} - Price: {item_details['price']}, Quantity: {item_details['quantity']}")
    else:
        print("Error fetching catalogue")

# Takes user input for stock name, order type, and quantity and sends a 
#POST request to the front-end service to place an order.
def place_order():
    stock_name = input("Enter stock name: ")
    order_type = input("Enter order type (BUY/SELL): ")
    quantity = input("Enter quantity: ")

    order_data = {
        'stock_name': stock_name,
        'order_type': order_type,
        'quantity': quantity
    }

    response = requests.post(FRONT_END_URL + '/place_order', json=order_data)
    if response.status_code == 200:
        transaction_number = response.json()['transaction_number']
        print(f"Order placed successfully. Transaction number: {transaction_number}")
    else:
        print("Failed to place order")

# Displays the menu and takes user input for their choice.
while True:
    print_menu()
    choice = input("Enter your choice: ")
    if choice == "1":
        view_catalogue()
    elif choice == "2":
        place_order()
    elif choice == "3":
        break
    else:
        print("Invalid choice. Please try again.")
