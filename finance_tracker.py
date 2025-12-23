import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import os

FILE_NAME = "expenses.csv"

# ---------- File Setup ----------
def ensure_file_exists():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "description", "amount"])

# ---------- Add Expense ----------
def add_expense(date, category, description, amount):
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, category, description, amount])

# ---------- Read All Expenses ----------
def read_expenses():
    expenses = []
    with open(FILE_NAME, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(row)
    return expenses

# ---------- GUI App ----------
class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        ensure_file_exists()
        self.build_ui()
        self.load_expenses()

    # ---------- UI ----------
    def build_ui(self):
        tk.Label(self.root, text="Personal Finance Tracker",
                 font=("Arial", 16, "bold")).pack(pady=10)

        form = tk.Frame(self.root)
        form.pack(pady=5)

        tk.Label(form, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
        tk.Label(form, text="Category").grid(row=0, column=1)
        tk.Label(form, text="Description").grid(row=0, column=2)
        tk.Label(form, text="Amount").grid(row=0, column=3)

        self.date_entry = tk.Entry(form, width=12)
        self.category_entry = tk.Entry(form, width=12)
        self.desc_entry = tk.Entry(form, width=20)
        self.amount_entry = tk.Entry(form, width=10)

        self.date_entry.grid(row=1, column=0, padx=5)
        self.category_entry.grid(row=1, column=1, padx=5)
        self.desc_entry.grid(row=1, column=2, padx=5)
        self.amount_entry.grid(row=1, column=3, padx=5)

        tk.Button(form, text="Add Expense",
                  command=self.add_expense_ui).grid(row=1, column=4, padx=5)

        # Table
        columns = ("date", "category", "description", "amount")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)

        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150)

        self.tree.pack(pady=10)

        # Report buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Monthly Report",
                  command=self.monthly_report).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="Export Monthly CSV",
                  command=self.export_monthly_report).grid(row=0, column=1, padx=10)

    # ---------- Load Expenses ----------
    def load_expenses(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for exp in read_expenses():
            self.tree.insert("", "end",
                             values=(exp["date"], exp["category"],
                                     exp["description"], exp["amount"]))

    # ---------- Add Expense UI ----------
    def add_expense_ui(self):
        date = self.date_entry.get().strip()
        category = self.category_entry.get().strip()
        desc = self.desc_entry.get().strip()
        amount = self.amount_entry.get().strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")
            amount = float(amount)
        except:
            messagebox.showerror("Error", "Invalid date or amount")
            return

        if not category or not desc:
            messagebox.showerror("Error", "All fields are required")
            return

        add_expense(date, category, desc, amount)
        self.load_expenses()

        self.date_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    # ---------- Monthly Report ----------
    def monthly_report(self):
        expenses = read_expenses()
        if not expenses:
            messagebox.showinfo("Info", "No expenses found")
            return

        month = tk.simpledialog.askinteger("Month", "Enter month (1-12):")
        year = tk.simpledialog.askinteger("Year", "Enter year:")

        if not month or not year:
            return

        category_totals = {}
        total = 0

        for exp in expenses:
            y, m, _ = exp["date"].split("-")
            if int(y) == year and int(m) == month:
                amt = float(exp["amount"])
                total += amt
                category_totals[exp["category"]] = category_totals.get(exp["category"], 0) + amt

        if not category_totals:
            messagebox.showinfo("Info", "No expenses for this month")
            return

        report = f"Monthly Report {year}-{month:02d}\n\n"
        for cat, amt in category_totals.items():
            report += f"{cat}: ₹{amt:.2f}\n"

        report += f"\nGrand Total: ₹{total:.2f}"
        messagebox.showinfo("Report", report)

    # ---------- Export Monthly ----------
    def export_monthly_report(self):
        expenses = read_expenses()
        if not expenses:
            messagebox.showinfo("Info", "No expenses found")
            return

        month = tk.simpledialog.askinteger("Month", "Enter month (1-12):")
        year = tk.simpledialog.askinteger("Year", "Enter year:")

        if not month or not year:
            return

        filename = f"report_{year}_{month:02d}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "description", "amount"])

            for exp in expenses:
                y, m, _ = exp["date"].split("-")
                if int(y) == year and int(m) == month:
                    writer.writerow(exp.values())

        messagebox.showinfo("Exported", f"Report saved as {filename}")

# ---------- Run ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()
