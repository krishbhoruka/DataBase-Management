import mysql.connector
import subprocess


# Function to connect to the database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database="retail_shop",
            user='root',
            password='Bhoruka@123'
        )
        print("Connected to the database!")
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return None


def add_product(connection):
    print("Add Product:")
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    quantity = int(input("Enter product quantity: "))
    category_id = int(input("Enter category ID: "))  # Assuming category ID is provided
    supplier_id = int(input("Enter supplier ID: "))  # Assuming supplier ID is provided
    store_id = int(input("Enter store ID: "))  # Assuming store ID is provided

    try:
        cursor = connection.cursor()

        # Insert the product details into the database
        cursor.execute("INSERT INTO product (name, price, quantity, category_id, supplier_id, store_id) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, price, quantity, category_id, supplier_id, store_id))
        connection.commit()
        print("Product added successfully!\n")

    except mysql.connector.Error as err:
        print("Error adding product:", err)

def check_product_exists(cursor, product_id):
    cursor.execute("SELECT COUNT(*) FROM product WHERE product_id = %s", (product_id,))
    count = cursor.fetchone()[0]
    return count > 0

def remove_product(connection):
    print("Remove Product:")
    product_id = int(input("Enter product ID to remove: "))

    try:
        cursor = connection.cursor()

        # Check if the product exists
        if not check_product_exists(cursor, product_id):
            print("Product does not exist.\n")
            return

        # Delete the product from the database
        cursor.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
        connection.commit()
        print("Product removed successfully!\n")

    except mysql.connector.Error as err:
        print("Error removing product:", err)

def update_product_quantity(connection):
    print("Update Product Quantity:")
    product_id = int(input("Enter product ID: "))
    new_quantity = int(input("Enter new quantity: "))

    try:
        cursor = connection.cursor()

        # Check if the product exists
        if not check_product_exists(cursor, product_id):
            print("Product does not exist.\n")
            return

        # Update the quantity of the product in the database
        cursor.execute("UPDATE product SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
        connection.commit()
        print("Product quantity updated successfully!\n")

    except mysql.connector.Error as err:
        print("Error updating product quantity:", err)

def main():
    connection = connect_to_database()
    if not connection:
        return


    while True:
        print("1. View Inventory")
        print("2. Add Product")
        print("3. Update Product Quantity")
        print("4. Remove Product")
        print("5. Back")
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            subprocess.run(["python3", "DBMS_5/inventory_analysis.py"])
        elif choice == '2':
            add_product(connection)
        elif choice == '3':
            update_product_quantity(connection)
        elif choice == '4':
            remove_product(connection)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.\n")

    connection.close()

if __name__ == "__main__":
    main()