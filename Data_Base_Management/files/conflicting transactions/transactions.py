import mysql.connector

def t1(cursor, db_connection):
    try:
        # Start Transaction 1
        cursor.execute("START TRANSACTION")
        cursor.execute("INSERT INTO customer (mail_id, phone_number, customer_pass, address_id) VALUES ('john.doe@example.com', '1234567890', 'Password123', 1)")
        cursor.execute("INSERT INTO customer (mail_id, phone_number, customer_pass, address_id) VALUES ('jane.doe@example.com', '9876543210', 'Password456', 2)")
        cursor.execute("COMMIT")

    except mysql.connector.Error as err:
        print("Error in Transaction 1:", err)
        db_connection.rollback()


def t2(cursor, db_connection):
    try:
        # Start Transaction 2
        cursor.execute("START TRANSACTION")
        cursor.execute("UPDATE product SET quantity = 20 WHERE product_id = 1")
        cursor.execute("INSERT INTO cart(customer_id, product_id, quantity) VALUES (1, 1, 50)")
        cursor.execute("COMMIT")

    except mysql.connector.Error as err:
        print("Error in Transaction 2:", err)
        db_connection.rollback()

def t3(cursor, db_connection):
    try:
        # Start Transaction 3
        cursor.execute("START TRANSACTION")
        cursor.execute("INSERT INTO cart(customer_id, product_id, quantity) VALUES (1, 2, 5)")
        cursor.execute("INSERT INTO cart(customer_id, product_id, quantity) VALUES (2, 2, 20)")
        cursor.execute("COMMIT")

    except mysql.connector.Error as err:
        print("Error in Transaction 3:", err)
        db_connection.rollback()

def t4(cursor, db_connection):
    try:
        # Start Transaction 4
        cursor.execute("START TRANSACTION")
        cursor.execute("UPDATE partner SET status = 1 WHERE partner_id = 1")
        cursor.execute("UPDATE partner SET status = 1 WHERE partner_id = 1")
        cursor.execute("COMMIT")

    except mysql.connector.Error as err:
        print("Error in Transaction 4:", err)
        db_connection.rollback()

def main():
    db_connection = mysql.connector.connect(
        host='127.0.0.1',
        database="retail_shop",
        user='root',
        password='Bhoruka@123'
    )

    cursor = db_connection.cursor()
    t4(cursor, db_connection)

    # Close cursor and database connection
    cursor.close()
    db_connection.close()

# Execute the main function
if __name__ == "__main__":
    main()
