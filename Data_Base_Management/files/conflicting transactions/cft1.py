import mysql.connector

db_connection = mysql.connector.connect(
        host='127.0.0.1',
        database="retail_shop",
        user='root',
        password='Bhoruka@123'
    )

cursor = db_connection.cursor()

try:
    # Start Transaction 1
    cursor.execute("START TRANSACTION")
    cursor.execute("INSERT INTO customer (mail_id, phone_number, customer_pass, address_id) VALUES ('jahn.doe@example.com', '1234560890', 'Password123', 1)")
    cursor.execute("INSERT INTO customer (mail_id, phone_number, customer_pass, address_id) VALUES ('jahn.doe@example.com', '9876543210', 'Password456', 2)")
    cursor.execute("COMMIT")

except mysql.connector.Error as err:
    print("Error in Transaction 1:", err)
    db_connection.rollback()
finally:
    cursor.close()
    db_connection.close()
