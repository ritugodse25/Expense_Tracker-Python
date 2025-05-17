# Expense_Tracker-Python
A simple command-line expense tracking application built with Python. This application helps you track your expenses, view summaries, and visualize spending patterns
## Features

- Add expenses with amount, category, and description
- View all expenses in chronological order
- Generate monthly expense summaries by category
- Visualize expenses with category-wise bar charts
- Data persistence using SQLite database

## Requirements

- Python 3.6 or higher
- Required packages listed in `requirements.txt`

## Installation

1. Clone or download this repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
python expense_tracker.py
```

The application provides a menu-driven interface with the following options:
1. Add Expense - Record a new expense
2. View All Expenses - Display all recorded expenses
3. View Monthly Summary - See expense totals by category for each month
4. Plot Expenses by Category - Generate a bar chart visualization
5. Exit - Close the application

## Data Storage

All expenses are stored in a SQLite database (`expenses.db`) which is automatically created when you first run the application.

## Visualization

When you choose to plot expenses, a bar chart is generated and saved as 'expense_summary.png' in the application directory.
