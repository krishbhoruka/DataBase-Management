import mysql.connector

# Function to validate login credentials
def login(mydb, phone_number, password):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM customer WHERE phone_number = %s AND customer_pass = %s", (phone_number, password))
        user = cursor.fetchone()
        if user:
            print("Login successful.\n")
            return True
        else:
            print("Invalid phone number or password. Please try again.")
            return False
    except Exception as e:
        print("Error:", e)
        return False

# Function to display available items
def display_items(mydb):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM product")
        items = cursor.fetchall()
        print("Available Items:")
        for item in items:
            print(f"Product ID: {item[0]}, Name: {item[4]}, Price: ${item[5]}, Stock Quantity: {item[6]}")
    except Exception as e:
        print("Error:", e)

# Function to add items to the cart
def add_to_cart(mydb, item_id, quantity,customer_id):
    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO cart (customer_id,product_id, quantity) VALUES (%s,%s, %s)", (customer_id,item_id, quantity))
        print("Item added to the cart successfully.")
        mydb.commit()
    except Exception as e:
        print("Error:", e)


# Function to view items in the cart
def view_cart(mydb, customer_id):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM cart WHERE customer_id=%s", (customer_id,))
        items = cursor.fetchall()
        if items:
            print("Items in Cart:")
            for item in items:
                print(f"Item ID: {item[1]}, Quantity: {item[2]}, Total Price: ${item[3]}")
            cursor.execute("SELECT total_amount FROM cart_total_amount WHERE customer_id=%s", (customer_id,))
            total_amount = cursor.fetchone()[0]
            print(f"Total Amount in Cart: ${total_amount}")
        else:
            print("Cart is empty.")
    except Exception as e:
        print("Error:", e)


def get_customer_id(mydb, phone_number):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT customer_id FROM customer WHERE phone_number = %s", (phone_number,))
        result = cursor.fetchone()
        if result:
            return result[0]  # Returns the customer_id if found
        else:
            print("Customer not found.")
            return None
    except Exception as e:
        print("Error:", e)
        return None

import mysql.connector
from datetime import datetime

# Dictionary to map payment modes to integer values
payment_modes = {
    1: 'cash',
    2: 'credit/debit card',
    3: 'online QR code'
}

def pay_option(mydb, customer_id):
    payment_modes = {
    1: 'cash',
    2: 'credit/debit card',
    3: 'online QR code'
    }
    try:
        print("Choose payment mode:")
        for key, value in payment_modes.items():
            print(f"{key}. {value}")
        print("\n")
        payment_choice = int(input("Enter the number corresponding to your preferred payment mode: "))
        if payment_choice in payment_modes:
            payment_type = payment_modes[payment_choice]
            cursor = mydb.cursor()
            payment_date = datetime.now().date()
            cursor.execute("INSERT INTO payment (customer_id, payment_type, payment_date) VALUES (%s, %s, %s)", (customer_id, payment_type, payment_date))
            mydb.commit()
            print("\nPayment completed successfully.\n")
            print("Your Order Will be Delivered Soon!!!\n")
            print("Cart Emptied\n")
        else:
            print("Invalid payment mode choice. Please choose a valid number.\n")
    except Exception as e:
        print("Error:", e)


def remove_product(mydb, customer_id):
    view_cart(mydb, customer_id)
    item_id = int(input("Enter the product_id to remove: "))
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM cart WHERE customer_id = %s AND product_id = %s", (customer_id, item_id))
        print("Item removed from cart successfully.")
        mydb.commit()
    except Exception as e:
        print("Error:", e)




# Main function
def main():
    try:
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            database="retail_shop",
            user='root',
            password='Bhoruka@123'
        )

        if mydb:
            # Login process
            while True:
                print()
                phone_number = input("Enter your phone number: ")
                password = input("Enter your password: ")
                if login(mydb, phone_number, password):
                    break
            customer_id=get_customer_id(mydb,phone_number)
            
            while True:
                choice=int(input("1. View Itmes\n2. Add Products\n3. View Cart\n4. To Pay\n5. Remove Product\n6. Log Out\n"))
                if choice==1:
                    display_items(mydb)
                elif choice==2:
                    item_id = int(input("Enter the item ID you want to order: "))
                    quantity = int(input("Enter the quantity you want to order: "))
                    add_to_cart(mydb, item_id, quantity,customer_id)
                elif choice==3:
                    view_cart(mydb,customer_id)
                elif choice==4:
                    pay_option(mydb,customer_id)
                elif choice==5:
                    remove_product(mydb,customer_id)
                elif choice==6:
                    break
                else:
                    print("Invalid Option")
            print("\n\nLogging Out.....")
            print("Thank You For Visiting")
            mydb.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
