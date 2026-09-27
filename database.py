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

    cursor.execute("""
        SELECT * FROM expenses
        ORDER BY date DESC,id DESC
        """)
    expenses = cursor.fetchall()
    connection.close()
    return expenses

def get_monthly_expenses(start_date,end_date):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id,date,amount ,category,description
        FROM expenses
        WHERE date >= ? AND date < ?
        ORDER BY date
        """,(start_date,end_date))
    
    expense = cursor.fetchall()
    connection.close()
    return expense

def delete_expense(expense_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )
    connection.commit()
    connection.close()
    
if __name__ == "__main__":
    initialize_database()
    
    # print("Database initialized successfully.")
    # print("Expense added successfully.")
    
    expenses = get_monthly_expenses(
        "2026-09-01",
        "2026-10-01"
    )
    print("September Expenses:")
    print(expenses)

