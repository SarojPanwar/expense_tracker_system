import sqlite3

def get_connection():
    connection = sqlite3.connect("expenses.db")
    return connection

def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS EXPENSES(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount INTEGER NOT NULL,
                category TEXT NOT NULL,
                description TEXT
                )
                """)
    connection.commit()
    connection.close()

def add_expense(date,amount,category,description):
    connection =get_connection()
    cursor= connection.cursor()

    cursor.execute("""
            INSERT INTO expenses (date,amount ,category,description)
            VALUES (?,?,?,?)
            """, (date,amount,category,description))

    connection.commit()
    connection.close()

def get_expenses():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    connection.close()
    return expenses

if __name__ == "__main__":
    initialize_database()
    
    # print("Database initialized successfully.")
    # print("Expense added successfully.")
    
    expenses = get_expenses()
    print("Expenses:")
    print(expenses)

