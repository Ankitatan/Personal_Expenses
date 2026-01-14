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
├── data_generation/
│   └── generate_expenses.py
│
├── database/
│   └── expenses.db
│
├── sql_queries/
│   └── analysis_queries.sql
│
├── app/
│   └── streamlit_app.py
│
├── requirements.txt
└── README.md
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

### Step 3: Generate Expense Data

```bash
python data_generation/generate_expenses.py
```

### Step 4: Run the Streamlit App

```bash
streamlit run app/streamlit_app.py
```

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
