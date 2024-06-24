import mysql.connector

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

def register_customer(connection):
    print("Customer Registration:")
    mail_id = input("Enter your email address: ")
    city = input("Enter your city: ")
    pincode = input("Enter your pincode: ")
    state = input("Enter your state: ")
    phone_number = input("Enter your phone number: ")
    customer_pass = input("Enter your password (between 8 and 20 characters, alphanumeric): ")

    try:
        cursor = connection.cursor()

        # Insert address details into the address table
        cursor.execute("INSERT INTO address (city, pincode, state) VALUES (%s, %s, %s)", (city, pincode, state))
        connection.commit()

        # Retrieve the auto-incremented address_id
        address_id = cursor.lastrowid

        # Insert the customer details into the customer table
        cursor.execute("INSERT INTO customer (mail_id, address_id, phone_number, customer_pass) VALUES (%s, %s, %s, %s)",
                       (mail_id, address_id, phone_number, customer_pass))
        connection.commit()
        print("Registration successful!")

    except mysql.connector.Error as err:
        print("Error registering customer:", err)

    finally:
        if cursor:
            cursor.close()


def main():
    connection = connect_to_database()
    if not connection:
        return
    register_customer(connection)
    connection.close()

if __name__ == "__main__":
    main()
