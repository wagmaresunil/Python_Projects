import mysql.connector
from mysql.connector import Error
import sys

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='sunil',
            user='root',
            password='Wsunil@$1995'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        sys.exit(1)

def show_menu():
    print("\n=== MySQL Python CRUD Operations ===")
    print("1. Insert")
    print("2. Update")
    print("3. Delete")
    print("4. Select All")
    print("5. Exit")

def insert_record(conn):
    cursor = conn.cursor()
    name = input("Name: ")
    age = int(input("Age: "))
    city = input("City: ")
    
    query = "INSERT INTO users (NAME, AGE, CITY) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, age, city))
    conn.commit()
    print("Record inserted successfully!")
    cursor.close()

def update_record(conn):
    cursor = conn.cursor()
    user_id = int(input("ID to update: "))
    name = input("New Name: ")
    age = int(input("New Age: "))
    city = input("New City: ")
    
    query = "UPDATE users SET NAME=%s, AGE=%s, CITY=%s WHERE ID=%s"
    cursor.execute(query, (name, age, city, user_id))
    conn.commit()
    print("Record updated successfully!")
    cursor.close()

def delete_record(conn):
    cursor = conn.cursor()
    user_id = int(input("ID to delete: "))
    
    query = "DELETE FROM users WHERE ID=%s"
    cursor.execute(query, (user_id,))
    conn.commit()
    print("Record deleted successfully!")
    cursor.close()

def select_all(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    
    print("\nAll Records:")
    print("ID | NAME | AGE | CITY")
    print("-" * 30)
    
    for (id, name, age, city) in cursor:
        print(f"{id} | {name} | {age} | {city}")
    
    cursor.close()

def main():
    conn = connect_db()
    
    while True:
        show_menu()
        choice = input("Enter choice: ")
        
        if choice == '1':
            insert_record(conn)
        elif choice == '2':
            update_record(conn)
        elif choice == '3':
            delete_record(conn)
        elif choice == '4':
            select_all(conn)
        elif choice == '5':
            print("Exiting...")
            conn.close()
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()