import mysql.connector

db_connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Bhoruka@123',
    database='retail_shop'
)

cursor = db_connection.cursor()

try:
    # Transaction 1: Insert customer and address
    cursor.execute("START TRANSACTION")
    cursor.execute(
        "INSERT INTO customer (mail_id, phone_number, customer_pass, address_id) VALUES ('joh456n.doe@exmple.com', '1234007790', 'Password123', 1)"
    )
    cursor.execute(
        "INSERT INTO address (city, pincode, state) VALUES ('New York', 10001, 'NY')"
    )
    cursor.execute("COMMIT")


    # Transaction 2: Insert product and category
    cursor.execute("START TRANSACTION")
    cursor.execute(
        "INSERT INTO product (category_id, supplier_id, store_id, name, price, quantity) VALUES (1, 1, 1, 'Laptop', 1000, 10)"
    )
    cursor.execute(
        "INSERT INTO category (category_name) VALUES ('Electronics')"
    )
    cursor.execute("COMMIT")


    # Transaction 3: Insert payment and orders
    cursor.execute("START TRANSACTION")
    cursor.execute(
        "INSERT INTO payment (customer_id, payment_type, payment_date) VALUES (1, 'Debit Card', '2023-03-16')"
    )
    cursor.execute(
        "INSERT INTO orders (customer_id, partner_id, order_date, amount) VALUES (1, 1, '2023-03-16', 200)"
    )
    cursor.execute("COMMIT")


    # Transaction 4: Insert supplier and product, then fetch products for the new supplier
    cursor.execute("START TRANSACTION")
    cursor.execute(
        "INSERT INTO supplier (name, phone_number) VALUES ('Supplier C', '9800543210')"
    )
    cursor.execute(
        "INSERT INTO product (category_id, supplier_id, store_id, name, price, quantity) VALUES (3, LAST_INSERT_ID(), 3, 'Cold Coffee', 100, 200)"
    )
    cursor.execute(
        "SELECT * FROM product WHERE supplier_id = LAST_INSERT_ID()"
    )
    cursor.execute("COMMIT")

    print("All transactions completed successfully")

except mysql.connector.Error as err:
    print("Error in transaction:", err)
    db_connection.rollback()  # Rollback in case of error

finally:
    # Ensure the connection and cursor are properly closed
    cursor.close()
    db_connection.close()
