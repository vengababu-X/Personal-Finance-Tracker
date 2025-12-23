<p align="center">
  <img src="assets/banner.gif" width="100%">
</p>

<h1 align="center">💰 Personal Finance Tracker</h1>

<p align="center">
  <b>Animated Python Desktop Application</b><br>
  <i>Expense Tracking • Monthly Reports • CSV Export</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue">
  <img src="https://img.shields.io/badge/GUI-Tkinter-green">
  <img src="https://img.shields.io/badge/Data-CSV-orange">
  <img src="https://img.shields.io/badge/Status-Completed-success">
</p>

---

## ✨ Application Preview

<p align="center">
  <img src="assets/app_demo.gif" width="75%">
</p>

> A full-featured Python desktop application that helps users record expenses, analyze monthly spending, and export financial reports.

---

## 🚀 Key Features

- 📥 Add daily expenses with date, category, description, and amount  
- 📋 View all expenses in a tabular format  
- 📆 Generate **monthly reports** (category-wise + total)  
- 📊 Automatic calculation of spending totals  
- 📤 Export monthly reports to CSV files  
- ⚠️ Input validation & error handling  
- 🖥️ User-friendly GUI (no terminal commands)

---

## 🧠 How the Application Works

<p align="center">
  <img src="assets/architecture.svg" width="85%">
</p>


---

## 🧾 Expense Management (Animated)

<p align="center">
  <img src="assets/add_expense.gif" width="70%">
</p>

- Enter expense details through GUI
- Date validation using `datetime`
- Data stored safely in CSV format

---

## 📊 Monthly Report Generation

<p align="center">
  <img src="assets/monthly_report.gif" width="70%">
</p>

- Select month and year
- View:
  - Category-wise totals
  - Grand total
- Prevents empty or invalid reports

---

## 📂 CSV Export Feature

<p align="center">
  <img src="assets/export.gif" width="70%">
</p>

- Automatically generates files like:


- Compatible with Excel and Google Sheets
- Demonstrates Python file handling

---

## 🛠️ Technologies Used

| Component | Technology |
|---------|-----------|
| Programming Language | Python 3 |
| GUI Framework | Tkinter |
| Tables & Widgets | ttk |
| Data Storage | CSV |
| Date Handling | datetime |
| Error Handling | try / except |

---

## 📂 Project Structure
Personal-Finance-Tracker/ │ ├── finance_tracker_app.py ├── expenses.csv ├── README.md └── assets/ ├── banner.gif ├── app_demo.gif ├── add_expense.gif ├── monthly_report.gif ├── export.gif └── architecture.svg

---

## ▶️ How to Run the Application

```bash
python finance_tracker_app.py
