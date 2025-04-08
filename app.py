from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os

app = Flask(__name__)

# CSV File Path
CSV_FILE = "expenses.csv"

# Ensure CSV exists with correct headers
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(CSV_FILE, index=False)

# Home Route - Display Expenses
@app.route('/')
def index():
    df = pd.read_csv(CSV_FILE)
    return render_template("index.html", expenses=df.to_dict(orient="records"))

# Add Expense Route
@app.route('/add', methods=['POST'])
def add_expense():
    date = request.form['date']
    category = request.form['category']
    amount = request.form['amount']
    description = request.form['description']

    df = pd.read_csv(CSV_FILE)
    new_expense = pd.DataFrame([[date, category, float(amount), description]], columns=df.columns)
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    return redirect(url_for('index'))

# Expense Analysis Route
@app.route('/analyze')
def analyze_expenses():
    df = pd.read_csv(CSV_FILE)

    if df.empty:
        return "<h2>No expenses to analyze!</h2>"

    plt.figure(figsize=(6, 6))
    df.groupby("Category")["Amount"].sum().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Expense Distribution")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template("analyze.html", plot_url=plot_url)

