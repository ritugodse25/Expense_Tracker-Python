import sqlite3
import datetime
from typing import List, Tuple
import matplotlib.pyplot as plt

class ExpenseTracker:
    def __init__(self):
        self.conn = sqlite3.connect('expenses.db')
        self.create_table()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL
        )
        ''')
        self.conn.commit()
    
    def add_expense(self, amount: float, category: str, description: str = '', date_str: str = ''):
        cursor = self.conn.cursor()
        if date_str:
            try:
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                print('Invalid date format. Please use YYYY-MM-DD format.')
                return
        else:
            date = datetime.date.today()
        cursor.execute(
            'INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)',
            (amount, category, description, date)
        )
        self.conn.commit()
        print(f'Added expense: ${amount:.2f} for {category} on {date}')
    
    def view_expenses(self) -> List[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        expenses = cursor.fetchall()
        if not expenses:
            print('No expenses found')
            return []
        
        print('\nAll Expenses:')
        print('ID | Date | Amount | Category | Description')
        print('-' * 50)
        for expense in expenses:
            print(f'{expense[0]} | {expense[4]} | ${expense[1]:.2f} | {expense[2]} | {expense[3]}')
        return expenses
    
    def monthly_summary(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT strftime('%Y-%m', date) as month,
               SUM(amount) as total,
               category
        FROM expenses
        GROUP BY month, category
        ORDER BY month DESC, total DESC
        ''')
        summary = cursor.fetchall()
        
        if not summary:
            print('No expenses found for monthly summary')
            return
        
        current_month = ''
        for month, total, category in summary:
            if month != current_month:
                print(f'\n=== {month} ===')
                current_month = month
            print(f'{category}: ${total:.2f}')
    
    def plot_expenses(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT category, SUM(amount) as total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
        ''')
        data = cursor.fetchall()
        
        if not data:
            print('No data available for plotting')
            return
        
        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]
        
        plt.figure(figsize=(10, 6))
        plt.bar(categories, amounts)
        plt.title('Expenses by Category')
        plt.xlabel('Categories')
        plt.ylabel('Amount ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('expense_summary.png')
        plt.close()
        print('\nExpense summary plot has been saved as "expense_summary.png"')

def main():
    tracker = ExpenseTracker()
    
    while True:
        print('\nExpense Tracker Menu:')
        print('1. Add Expense')
        print('2. View All Expenses')
        print('3. View Monthly Summary')
        print('4. Plot Expenses by Category')
        print('5. Exit')
        
        choice = input('\nEnter your choice (1-5): ')
        
        if choice == '1':
            try:
                amount = float(input('Enter amount: '))
                category = input('Enter category: ')
                description = input('Enter description (optional): ')
                date_str = input('Enter date (YYYY-MM-DD) or press Enter for today: ')
                tracker.add_expense(amount, category, description, date_str)
            except ValueError:
                print('Invalid amount. Please enter a number.')
        
        elif choice == '2':
            tracker.view_expenses()
        
        elif choice == '3':
            tracker.monthly_summary()
        
        elif choice == '4':
            tracker.plot_expenses()
        
        elif choice == '5':
            print('Thank you for using Expense Tracker!')
            break
        
        else:
            print('Invalid choice. Please try again.')

if __name__ == '__main__':
    main()