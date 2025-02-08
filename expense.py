import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

def create_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY,
                        amount REAL,
                        category TEXT,
                        description TEXT,
                        date TEXT)''')
    conn.commit()
    conn.close()

def add_expense(amount, category, description, date):
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format! Please use YYYY-MM-DD.")
        return
    
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)", (amount, category, description, formatted_date))
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_monthly_summary(month, year):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ? GROUP BY category", (month, year))
    summary = cursor.fetchall()
    conn.close()
    return summary

def delete_expense(expense_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    print("Expense deleted successfully!")

def plot_expense_graph(month, year):
    data = get_monthly_summary(month, year)
    if data:
        categories, amounts = zip(*data)
        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title(f'Expense Summary for {month}-{year}')
        plt.show()
    else:
        print("No expenses found for this month.")

# Initialize Database
create_db()

while True:
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. View Monthly Summary")
    print("5. Exit")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        try:
            amount = float(input("Enter expense amount: "))
            category = input("Enter expense category: ")
            description = input("Enter expense description: ")
            date = input("Enter expense date (YYYY-MM-DD): ")
            add_expense(amount, category, description, date)
            print("Expense added successfully!\n")
        except ValueError:
            print("Invalid input. Please enter a valid amount.\n")
    
    elif choice == "2":
        expenses = get_all_expenses()
        if expenses:
            print("\nAll Expenses:")
            for exp in expenses:
                print(f"ID: {exp[0]}, Amount: {exp[1]}, Category: {exp[2]}, Description: {exp[3]}, Date: {exp[4]}")
        else:
            print("No expenses recorded.")
    
    elif choice == "3":
        expense_id = input("Enter the ID of the expense to delete: ")
        if expense_id.isdigit():
            delete_expense(int(expense_id))
        else:
            print("Invalid ID. Please enter a valid numeric ID.")
    
    elif choice == "4":
        month = datetime.now().strftime('%m')
        year = datetime.now().strftime('%Y')
        print("\nMonthly Summary:")
        summary = get_monthly_summary(month, year)
        if summary:
            for category, amount in summary:
                print(f"{category}: ${amount:.2f}")
            plot_expense_graph(month, year)
        else:
            print("No expenses found for this month.")
    
    elif choice == "5":
        print("Exiting... Goodbye!")
        break
    else:
        print("Invalid choice! Please enter a valid option.")
