"""
Personal Finance Tracker - Intermediate Project

Features:
- Add expenses (date, category, description, amount)
- Save all expenses to a CSV file (expenses.csv)
- View all expenses
- View monthly summary (by year & month) with total per category + grand total
- Export monthly summary to a separate CSV file (report_YYYY_MM.csv)
- Basic error handling for file operations and user input

Concepts used:
- File handling (txt/csv)
- csv module
- Error handling (try/except)
- Functions and clean code structure
"""

import csv
import os
from datetime import datetime

EXPENSES_FILE = "expenses.csv"


# ------------- Utility Functions ------------- #

def ensure_file_exists():
    """
    Make sure the main CSV file exists and has a header row.
    """
    if not os.path.exists(EXPENSES_FILE):
        try:
            with open(EXPENSES_FILE, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # Header row
                writer.writerow(["date", "category", "description", "amount"])
        except IOError:
            print("❌ Error: Could not create expenses file.")


def parse_date(date_str):
    """
    Parse date string in format YYYY-MM-DD.
    If invalid, raise ValueError.
    """
    return datetime.strptime(date_str, "%Y-%m-%d")


def get_valid_date(prompt):
    """
    Keep asking until user gives a valid date in YYYY-MM-DD format.
    """
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            # default: today
            return datetime.today()
        try:
            return parse_date(date_str)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD (or press Enter for today).")


def get_valid_float(prompt):
    """
    Get a valid float from user; keep asking until valid.
    """
    while True:
        value = input(prompt).strip()
        try:
            amount = float(value)
            if amount <= 0:
                print("Amount must be positive.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a number.")


def get_non_empty_input(prompt):
    """
    Input that cannot be empty.
    """
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Input cannot be empty.")


# ------------- Core Finance Functions ------------- #

def add_expense():
    """
    Add a new expense and append it to the CSV file.
    """
    print("\n--- Add New Expense ---")
    date_obj = get_valid_date("Enter date (YYYY-MM-DD) or press Enter for today: ")
    category = get_non_empty_input("Enter category (e.g., Food, Travel, Shopping): ")
    description = input("Enter description (optional): ").strip()
    amount = get_valid_float("Enter amount: ")

    row = [
        date_obj.strftime("%Y-%m-%d"),
        category,
        description,
        f"{amount:.2f}"
    ]

    try:
        with open(EXPENSES_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        print("✅ Expense added successfully.")
    except IOError:
        print("❌ Error: Could not write to expenses file.")


def read_all_expenses():
    """
    Read all expenses from the CSV file.
    Returns a list of dicts: [{"date": ..., "category": ..., ...}, ...]
    """
    expenses = []
    if not os.path.exists(EXPENSES_FILE):
        print("No expenses file found yet.")
        return expenses

    try:
        with open(EXPENSES_FILE, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                expenses.append(row)
    except IOError:
        print("❌ Error: Could not read expenses file.")
    return expenses


def view_all_expenses():
    """
    Print all expenses in a readable format.
    """
    print("\n--- All Expenses ---")
    expenses = read_all_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    for idx, exp in enumerate(expenses, start=1):
        print(
            f"{idx}. Date: {exp['date']}, "
            f"Category: {exp['category']}, "
            f"Description: {exp['description']}, "
            f"Amount: ₹{exp['amount']}"
        )


def get_monthly_expenses(year, month):
    """
    Filter all expenses that match the given year and month.
    year: int, month: int
    Returns a list of expense dicts.
    """
    expenses = read_all_expenses()
    monthly = []
    for exp in expenses:
        try:
            date_obj = parse_date(exp["date"])
        except ValueError:
            # Skip bad data
            continue

        if date_obj.year == year and date_obj.month == month:
            monthly.append(exp)
    return monthly


def monthly_report():
    """
    Show monthly summary:
    - list of expenses
    - total per category
    - grand total
    Optionally export to CSV.
    """
    print("\n--- Monthly Report ---")
    # Get year and month from user
    while True:
        year_str = input("Enter year (YYYY): ").strip()
        if year_str.isdigit() and len(year_str) == 4:
            year = int(year_str)
            break
        print("Invalid year. Example: 2025")

    while True:
        month_str = input("Enter month (1-12): ").strip()
        if month_str.isdigit():
            month = int(month_str)
            if 1 <= month <= 12:
                break
        print("Invalid month. Enter a number between 1 and 12.")

    expenses = get_monthly_expenses(year, month)

    if not expenses:
        print(f"No expenses found for {year}-{month:02d}.")
        return

    print(f"\nExpenses for {year}-{month:02d}:")
    category_totals = {}
    grand_total = 0.0

    for idx, exp in enumerate(expenses, start=1):
        try:
            amount = float(exp["amount"])
        except ValueError:
            amount = 0.0
        grand_total += amount

        cat = exp["category"]
        category_totals[cat] = category_totals.get(cat, 0.0) + amount

        print(
            f"{idx}. Date: {exp['date']}, "
            f"Category: {exp['category']}, "
            f"Description: {exp['description']}, "
            f"Amount: ₹{amount:.2f}"
        )

    print("\n--- Category-wise Totals ---")
    for cat, total in category_totals.items():
        print(f"{cat}: ₹{total:.2f}")

    print(f"\nGrand Total: ₹{grand_total:.2f}")

    # Ask if user wants to export
    choice = input("\nExport this monthly report to CSV? (y/n): ").strip().lower()
    if choice == "y":
        export_monthly_report(expenses, year, month)
    else:
        print("Report not exported.")


def export_monthly_report(expenses, year, month):
    """
    Export given expenses list to a new CSV file named report_YYYY_MM.csv
    """
    filename = f"report_{year}_{month:02d}.csv"
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            fieldnames = ["date", "category", "description", "amount"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for exp in expenses:
                writer.writerow(exp)
        print(f"✅ Monthly report exported as {filename}")
    except IOError:
        print("❌ Error: Could not write report file.")


# ------------- Menu / Main Loop ------------- #

def print_menu():
    print("\n====== Personal Finance Tracker ======")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View Monthly Report")
    print("4. Exit")


def main():
    ensure_file_exists()

    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all_expenses()
        elif choice == "3":
            monthly_report()
        elif choice == "4":
            print("Exiting... Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()
