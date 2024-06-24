try:
    # Start Transaction 2
    cursor.execute("START TRANSACTION")
    cursor.execute("UPDATE product SET quantity = 20 WHERE product_id = 1")
    cursor.execute("INSERT INTO cart(customer_id, product_id, quantity) VALUES (1, 1, 50)")
    cursor.execute("COMMIT")

except mysql.connector.Error as err:
    print("Error in Transaction 2:", err)
    db_connection.rollback()