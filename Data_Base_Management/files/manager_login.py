import mysql.connector
import subprocess

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database="retail_shop",
            user='root',
            password='Bhoruka@123'
        )
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return None

def manager_login(connection):
    print("Manager Login:")
    phone_number = input("Enter your phone number: ")
    password = input("Enter your password: ")

    try:
        cursor = connection.cursor()

        # Query the database to verify credentials
        cursor.execute("SELECT * FROM Manager WHERE phone_number = %s AND password = %s", (phone_number, password))
        manager = cursor.fetchone()

        if manager:
            print("Login successful.\n")
            return manager
        else:
            print("Invalid phone number or password. Please try again.\n")
            return None

    except mysql.connector.Error as err:
        print("Error:", err)
        return None

def view_inventory(connection):
    subprocess.run(["python3", "DBMS_5/inventory_analysis.py"])

def modify_inventory(connection):
    subprocess.run(["python3", "DBMS_5/product_modification.py"])

def view_orders(connection):
    print("View all Orders:")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders;")
        orders = cursor.fetchall()
        
        # Print each order
        for order in orders:
            print("Order ID: ",order[0])
            print("Delivery Partner ID: ",order[1])
            print("Customer ID: ",order[2])
            print("Payment ID: ",order[3])
            print("Order Date: ",order[4])
            print("Amount: ",order[5])
            print("-------------------------")
        
    except mysql.connector.Error as err:
        print("Error fetching orders:", err)


def view_payments(connection):
    print("View all Payments:")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM payment;")
        payments = cursor.fetchall()
        
        for payment in payments:
            print("Payment ID: ",payment[0])
            print("Customer ID: ",payment[1])
            print("Payment Type: ",payment[2])
            print("Payment Date: ",payment[3])
            print("-------------------------")
        
    except mysql.connector.Error as err:
        print("Error fetching orders:", err)

def view_customer_details(connection):
    print("View Customer Details and Analysis:")
    subprocess.run(["python3","DBMS_5/customer_analysis.py"])

def display_options():
    print("Options:")
    print("1. View Inventory")
    print("2. Modify Inventory")
    print("3. View all Orders")
    print("4. View all Payments")
    print("5. View Customer Details and Analysis")
    print("6. Logout")

def main():
    connection = connect_to_database()
    if not connection:
        return

    manager = manager_login(connection)
    if not manager:
        return

    while True:
        display_options()
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            view_inventory(connection)
        elif choice == '2':
            modify_inventory(connection)
        elif choice == '3':
            view_orders(connection)
        elif choice == '4':
            view_payments(connection)
        elif choice == '5':
            view_customer_details(connection)
        elif choice == '6':
            print("Logout successful.")
            break
        else:
            print("Invalid choice. Please try again.\n")

    connection.close()

if __name__ == "__main__":
    main()
