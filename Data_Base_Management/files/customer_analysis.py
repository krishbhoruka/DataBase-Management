import mysql.connector

# Establishing the database connection
mydb = mysql.connector.connect(
    host='127.0.0.1',
    database="retail_shop",
    user='root',
    password='Bhoruka@123'
)

def main():
    print("Customer Details")
    cmd = """SELECT * FROM customer NATURAL JOIN customer_analysis;"""
    try:
        cursor = mydb.cursor()
        cursor.execute(cmd)
        rows = cursor.fetchall()
        for row in rows:
            print("Customer Id: ",row[0])
            print("Mail Id: ",row[1])
            print("Address Id: ",row[2])
            print("Phone Number: ",row[3])
            print("No of Orders: ",row[5])
            print("Total Order Values: ",row[6])
            print("Average Order Value: ",row[7])
            print("-------------------------")
    except mysql.connector.Error as error:
        print("Error executing SQL query:", error)
    finally:
        cursor.close()


if __name__ == "__main__":
    main()