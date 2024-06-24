import mysql.connector

# Establishing the database connection
mydb = mysql.connector.connect(
    host='127.0.0.1',
    database="retail_shop",
    user='root',
    password='Bhoruka@123'
)

def main():
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM product")
        low_inventory_products = cursor.fetchall()
        if low_inventory_products:
            print("\n\n\nProducts Available:\n")
            for product in low_inventory_products:
                print("Product ID:", product[0])
                print("Name:", product[4])
                print("Quantity:", product[6])
                print("Price:", product[5])
                print("Supplier_ID:", product[2])
                print("-------------------------")
        else:
            print("No products.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()


# Entry point of the program
if __name__ == "__main__":
    main()
