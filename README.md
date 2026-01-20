# Personal Expenses Analysis Project

## Overview

The **Personal Expenses Analysis** project is an end-to-end data analytics application designed to simulate, store, analyze, and visualize personal financial transactions. The project demonstrates practical use of **Python, SQL, and Streamlit** to derive insights into spending behavior and support better financial decision-making.

This project is suitable for showcasing skills in **data analysis, data engineering, SQL querying, and dashboard development**, particularly for roles such as Data Analyst or Aspiring Data Scientist.

---

## Objectives

* Generate realistic personal expense data using synthetic data tools
* Store and manage transactional data in a relational database
* Perform analytical queries to uncover spending patterns
* Build an interactive dashboard for financial insights
* Enable users to track expenses, categories, trends, and budgets

---

## Tech Stack

* **Programming Language:** Python
* **Database:** SQLite / MySQL (configurable)
* **Libraries & Tools:**

  * Pandas
  * Faker
  * SQLite3 / MySQL Connector
  * Streamlit
  * Matplotlib / Plotly
* **IDE:** VS Code / Jupyter Notebook

---

## Project Architecture

```
Personal_Expenses_Analysis/
│
├── __pycache__/                  # Python cache files
├── analytics_charts.py           # Script for creating charts/visualizations
├── analytics_queries.py          # SQL queries or analytics scripts
├── EDA_personal_expenses.ipynb   # EDA 
├── data_simulation.py            # Script to generate synthetic expense data
├── Expense_tracker_project_doc.pdf  # Project documentation
├── expenses/                     # Folder for storing processed expense files
├── expenses                      # Possibly another data or config file (check extension)
├── expenses_month_1.xlsx         # Monthly expense data
├── expenses_month_2.xlsx
├── expenses_month_3.xlsx
├── expenses_month_4.xlsx
├── expenses_month_5.xlsx
├── expenses_month_6.xlsx
├── expenses_month_7.xlsx
├── expenses_month_8.xlsx
├── expenses_month_9.xlsx
├── expenses_month_10.xlsx
├── expenses_month_11.xlsx
├── expenses_month_12.xlsx
├── Financial_Tracker_and_Planner.pdf  # Additional documentation/planner
├── init_db.py                    # Script to initialize the database
├── requirements.txt              # Python dependencies
└── streamlit_app.py              # Streamlit dashboard application
```

---

## Dataset Description

The dataset represents personal financial transactions and includes the following fields:

* **Transaction ID**
* **Date**
* **Category** (Groceries, Rent, Travel, Entertainment, Utilities, etc.)
* **Amount**
* **Payment Mode** (Cash, Credit Card, UPI, Debit Card)
* **Merchant / Description**
* **Cashback / Rewards (if applicable)**

Data is generated using the **Faker** library to closely mimic real-world expense behavior.

---

## Key Features & Analysis

* Total spending by category
* Monthly and yearly expense trends
* Payment mode distribution
* High-priority vs low-priority spending
* Identification of recurring expenses
* Cashback and reward analysis
* Budget threshold alerts
* Comparative analysis across months

---

## SQL Analysis Examples

* Total expense by category
* Monthly spending trends
* Top 5 spending categories
* Average transaction value
* Recurring transactions detection

---

## Streamlit Dashboard

The Streamlit application provides:

* Interactive filters (date range, category, payment mode)
* Dynamic charts and KPIs
* Expense comparison across months
* Visual insights for better financial planning

---

## How to Run the Project

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd Personal_Expenses_Analysis
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Initialise the DB

```bash
python init_db.py
```

### Step 4: Generate Expense Data

```bash
python data_simulation.py
```
##### This script creates synthetic monthly expense data and populates the database.


### Step 5: Run EDA (Exploratory Data Analysis) File

```bash
python EDA_Personal_Expenses.py
```
##### You can optionally review the results as CSV/Excel outputs in the expenses/ folder.

### Step 6: Run the Streamlit App

```bash
streamlit run app/streamlit_app.py
```
##### Use interactive filters to explore expenses, trends, and budget insights.

---

## Use Cases

* Personal finance tracking
* Expense optimization and budgeting
* Demonstration project for data analytics portfolios
* SQL and dashboarding practice

---

## Future Enhancements

* User authentication and profiles
* Real-time expense input
* Cloud database integration
* Predictive expense forecasting
* Mobile-friendly dashboard

---

## Author

**Ankita Taneja**
Aspiring Data Scientist

---

## License

This project is for educational and portfolio purposes.
