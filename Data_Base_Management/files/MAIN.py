import subprocess

# Function to handle adminlogin
def admin_login():
    subprocess.run(["python3", "DBMS_5/APP.py"])

# Function to handle manager login
def manager_login():
    subprocess.run(["python3", "DBMS_5/manager_login.py"])

# Function to handle customer registration
def register_customer():
    subprocess.run(["python3", "DBMS_5/customer_registration.py"])

# Function to handle customer login
def customer_login():
    subprocess.run(["python3", "DBMS_5/customer_login.py"])

# Main function
def main():
    while True:
        print("\n\nMain Menu:")
        print("1. Admin Login")
        print("2. Login as Manager")
        print("3. Register as Customer")
        print("4. Login as Customer")
        print("5. Exit")

        choice = input("Please enter your choice (1-4): ")
        if choice=='1':
            admin_login()
        if choice == '2':
            manager_login()
        elif choice == '3':
            register_customer()
        elif choice == '4':
            customer_login()
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
