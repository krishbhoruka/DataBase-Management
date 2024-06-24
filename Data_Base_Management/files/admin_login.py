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

def register_manager(admin_id,connection):
    print("Manager Registration:")
    name = input("Enter your name: ")
    city = input("Enter your city: ")
    pincode = input("Enter your pincode: ")
    state = input("Enter your state: ")
    phone_number = input("Enter your phone number: ")
    password = input("Enter your password (between 8 and 20 characters, alphanumeric): ")

    try:
        cursor = connection.cursor()

        # Insert address details into the address table
        cursor.execute("INSERT INTO address (city, pincode, state) VALUES (%s, %s, %s)", (city, pincode, state))
        connection.commit()

        # Retrieve the auto-incremented address_id
        address_id = cursor.lastrowid

        # Insert the customer details into the customer table
        cursor.execute("INSERT INTO manager (address_id, admin_id, name, password, phone_number) VALUES (%s, %s, %s, %s, %s)",
               (address_id, admin_id, name, password, phone_number))
        connection.commit()
        print("Manager Registration successful!")

    except mysql.connector.Error as err:
        print("Error registering customer:", err)

    finally:
        if cursor:
            cursor.close()

def admin_login(connection,admin_id,password):
    try:
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM admin where admin_id=%s AND admin_pass=%s",(admin_id,password))
        admin=cursor.fetchone()
        if admin:
            print("Admin Login Successfull!\n")
            return True
        else:
            return False
    except Exception as e:
        print("Error:", e)
        return False

def display_options():
    print("Options:")
    print("1. View Inventory")
    print("2. Modify Inventory")
    print("3. View all Orders")
    print("4. View all Payments")
    print("5. View Customer Details and Analysis")
    print("6. Register Manager")
    print("7. View Managers")
    print("8. Logout")


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

def view_managers(connection):
    print("\n\nManager Details\n")
    cmd = """SELECT * FROM manager;"""
    try:
        cursor=connection.cursor()
        cursor.execute(cmd)
        rows=cursor.fetchall()
        for row in rows:
            print("Manager ID: ",row[0])
            print("Name ",row[3])
            print("Phone Number ",row[5])
            print("-------------------------")
    except mysql.connector.Error as error:
        print("Error executing SQL query:", error)
    finally:
        cursor.close()


def main():
    connection = connect_to_database()
    if not connection:
        return
    
    admin_id=int(input("Enter Admin ID: "))
    password=input("Enter Password: ")
    if admin_login(connection,admin_id,password):
        while True:
            display_options()
            choice = input("\nEnter your choice (1-6): ")
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
                register_manager(admin_id,connection)
            elif choice == '7':
                view_managers(connection)
            elif choice == '8':
                print("Logout successful.")
                break
            else:
                print("Invalid choice. Please try again.\n")
            
    else:
        print("Invalid admin id or password.")
    connection.close()


if __name__ == "__main__":
    main()
