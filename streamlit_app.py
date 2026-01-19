import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

DB_PATH = "expenses.db"

# ---------------- DATABASE FUNCTIONS -----------------
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            payment_mode TEXT,
            description TEXT,
            amount REAL,
            cashback REAL
        )
    """)
    conn.commit()
    conn.close()

def load_expenses():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM expenses", conn)
    conn.close()
    return df

def insert_expense(date, category, payment_mode, desc, amount, cashback):
    conn = get_connection()
    conn.execute("""
        INSERT INTO expenses (date, category, payment_mode, description, amount, cashback)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, category, payment_mode, desc, amount, cashback))
    conn.commit()
    conn.close()


# ---------------- APP CONFIG -------------------------
st.set_page_config(page_title="Advanced Expense Dashboard", layout="wide")

# ----- CUSTOM CSS for MAROON ACTIVE TAB -----
# ---------------- CUSTOM CSS FOR TABS -----------------
st.markdown(
    """
    <style>
    /* Inactive tabs: light blue background, blue text, rounded, padding, border */
    div[data-baseweb="tab-list"] button {
        background-color: #87CEEB;   /* Light Sky Blue */
        color: #104E8B;               /* Dark Blue text */
        border-radius: 12px;         
        padding: 10px 20px;          
        border: 2px solid #104E8B;  
        font-weight: bold;           
        margin-right: 4px;           
        transition: all 0.3s ease;   
    }

    /* Active tab: white background, blue text, blue border */
    div[data-baseweb="tab-list"] button[data-selected="true"] {
        background-color: white;     
        color: #104E8B !important;   
        border-radius: 12px;
        padding: 10px 20px;
        border: 2px solid #104E8B;  
        font-weight: bold;
        transition: all 0.3s ease;   
    }

    /* Hover effect for inactive tabs */
    div[data-baseweb="tab-list"] button:hover {
        background-color: #104E8B;  
        color: white;
        transition: all 0.3s ease;   
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💰 ADVANCED PERSONAL EXPENSE DASHBOARD")
st.write("Analyze your expenses with SQL-powered insights, filters, charts & KPIs.")

create_table()
df = load_expenses()

# ---------------- FILTER SIDEBAR -------------------
st.sidebar.header("🔍 Filters")

if not df.empty:
    categories = ["All"] + sorted(df["category"].unique().tolist())
    payment_modes = ["All"] + sorted(df["payment_mode"].unique().tolist())

    selected_category = st.sidebar.selectbox("Filter by Category:", categories)
    selected_payment = st.sidebar.selectbox("Filter by Payment Mode:", payment_modes)
    selected_month = st.sidebar.selectbox("Filter by Month:",
                                          ["All"] + sorted(df['date'].str.slice(0, 7).unique().tolist()))

    filtered_df = df.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]
    if selected_payment != "All":
        filtered_df = filtered_df[filtered_df["payment_mode"] == selected_payment]
    if selected_month != "All":
        filtered_df = filtered_df[filtered_df["date"].str.startswith(selected_month)]
else:
    filtered_df = pd.DataFrame()


# -------------------- TABS ------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📊 Dashboard", "🧮 SQL 15 Queries", "🔢 SQL Add-on Queries", "➕ Add Expense",
     "📄 Raw Data", "⬇️ Download"]
)

# ---------------- TAB 1 — DASHBOARD ----------------
with tab1:
    st.header("📊 Expense Overview")

    if filtered_df.empty:
        st.warning("No data available. Add records in 'Add Expense' tab.")
    else:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Spending", f"₹{filtered_df['amount'].sum():,.2f}", delta_color="inverse")
        col2.metric("Transactions", len(filtered_df))
        col3.metric("Total Cashback", f"₹{filtered_df['cashback'].sum():,.2f}", delta_color="inverse")
        col4.metric("Avg Transaction", f"₹{filtered_df['amount'].mean():,.2f}", delta_color="inverse")

        # Category Chart
        st.subheader("📌 Spending by Category")
        cat_data = filtered_df.groupby("category")["amount"].sum().reset_index()
        st.bar_chart(cat_data, x="category", y="amount")

        # Payment Mode Pie Chart
        st.subheader("💳 Payment Mode Distribution")
        pm_data = filtered_df.groupby("payment_mode")["amount"].sum().reset_index()
        fig = px.pie(pm_data, names="payment_mode", values="amount")
        st.plotly_chart(fig)

        # Monthly Trend
        st.subheader("📅 Monthly Spending Trend")
        filtered_df["month"] = filtered_df["date"].str.slice(0, 7)
        trend = filtered_df.groupby("month")["amount"].sum().reset_index()
        st.line_chart(trend, x="month", y="amount")


# ---------------- TAB 2 — SQL INSIGHTS ----------------
with tab2:
    st.header("🧮 SQL 15 Mandatory Queries")

    if df.empty:
        st.warning("Add some expenses to view SQL insights.")
    else:
        conn = get_connection()

        queries = {

            "1. What is the total amount spent in each category?": """
                SELECT category, ROUND(SUM(amount), 2) AS total_spent
                FROM expenses
                GROUP BY category
                ORDER BY total_spent DESC;
            """,

            "2. What is the total amount spent using each payment mode?": """
                SELECT payment_mode, ROUND(SUM(amount), 2) AS total_spent
                FROM expenses
                GROUP BY payment_mode;
            """,

            "3. What is the total cashback received across all transactions?": """
                SELECT ROUND(SUM(cashback), 2) AS total_cashback
                FROM expenses;
            """,

            "4. Which are the top 5 most expensive categories in terms of spending?": """
                SELECT category, ROUND(SUM(amount), 2) AS total_spent
                FROM expenses
                GROUP BY category
                ORDER BY total_spent DESC
                LIMIT 5;
            """,

            "5. How much was spent on transportation using different payment modes?": """
                SELECT payment_mode, ROUND(SUM(amount), 2) AS total_spent
                FROM expenses
                WHERE category = 'Transportation'
                GROUP BY payment_mode
                ORDER BY total_spent DESC;
            """,

            "6. Which transactions resulted in cashback?": """
                SELECT date, category, payment_mode, amount, cashback
                FROM expenses
                WHERE cashback > 0
                ORDER BY cashback DESC;
            """,

            "7. What is the total spending in each month of the year?": """
                SELECT SUBSTR(date, 1, 7) AS month,
                       ROUND(SUM(amount), 2) AS total_spent
                FROM expenses
                GROUP BY month
                ORDER BY month;
            """,

            "8. Which months have the highest spending in Travel, Entertainment, or Gifts?": """
                SELECT SUBSTR(date, 1, 7) AS month,
                       category,
                       ROUND(SUM(amount), 2) AS total_spent
                FROM expenses
                WHERE category IN ('Travel', 'Entertainment', 'Gifts')
                GROUP BY month, category
                ORDER BY total_spent DESC;
            """,

            "9. Are there any recurring expenses during specific months?": """
                SELECT description,
                       COUNT(*) AS frequency
                FROM expenses
                GROUP BY description
                HAVING frequency > 2
                ORDER BY frequency DESC;
            """,

            "10. How much cashback or rewards were earned in each month?": """
                SELECT SUBSTR(date, 1, 7) AS month,
                       ROUND(SUM(cashback), 2) AS total_cashback
                FROM expenses
                GROUP BY month
                ORDER BY month;
            """,

            "11. How has overall spending changed over time?": """
                WITH monthly_spend AS (
                    SELECT SUBSTR(date, 1, 7) AS month,
                           SUM(amount) AS total_spent
                    FROM expenses
                    GROUP BY month
                )
                SELECT month,
                       total_spent,
                       total_spent - LAG(total_spent) OVER (ORDER BY month) AS month_change
                FROM monthly_spend;
            """,

            "12. What are the typical costs for different travel types?": """
                SELECT description AS travel_type,
                       ROUND(AVG(amount), 2) AS avg_cost,
                       ROUND(MIN(amount), 2) AS min_cost,
                       ROUND(MAX(amount), 2) AS max_cost
                FROM expenses
                WHERE category = 'Travel'
                GROUP BY travel_type
                ORDER BY avg_cost DESC;
            """,

            "13. Are there patterns in grocery spending (weekday vs weekend)?": """
                SELECT 
                    CASE 
                        WHEN STRFTIME('%w', date) IN ('0','6') THEN 'Weekend'
                        ELSE 'Weekday'
                    END AS day_type,
                    ROUND(SUM(amount), 2) AS total_spent
                FROM expenses
                WHERE category = 'Grocery'
                GROUP BY day_type;
            """,

            "14. Define High and Low Priority Categories based on spending": """
                WITH category_spend AS (
                    SELECT category, SUM(amount) AS total_spent
                    FROM expenses
                    GROUP BY category
                ),
                ranked AS (
                    SELECT category,
                           total_spent,
                           NTILE(3) OVER (ORDER BY total_spent DESC) AS priority_rank
                    FROM category_spend
                )
                SELECT category,
                       total_spent,
                       CASE
                           WHEN priority_rank = 1 THEN 'High Priority'
                           WHEN priority_rank = 3 THEN 'Low Priority'
                           ELSE 'Medium Priority'
                       END AS priority_level
                FROM ranked
                ORDER BY total_spent DESC;
            """,

            "15. Which category contributes the highest percentage of total spending?": """
                SELECT category,
                       ROUND(SUM(amount) * 100.0 / 
                            (SELECT SUM(amount) FROM expenses), 2) AS percentage_contribution
                FROM expenses
                GROUP BY category
                ORDER BY percentage_contribution DESC
                LIMIT 1;
            """
        }

        selected_query = st.selectbox(
            "Select a query to run:",
            list(queries.keys()),
            key="query_selector_tab2"
        )

        if st.button("Run Query", key="run_query_tab2"):
            result = pd.read_sql_query(queries[selected_query], conn)
            st.dataframe(result, use_container_width=True)

        conn.close()


# ---------------- TAB 3 — SQL Add-ons Queries ----------------
with tab3:
    st.header("🔢 SQL Add-ons Queries (Self-Created)")

    if df.empty:
        st.warning("Add some expenses to view SQL insights.")
    else:
        conn = get_connection()

        queries = {

            "1. Which day of the week has the highest average spending?": """
                SELECT strftime('%w', date) AS day_of_week,
                       ROUND(AVG(amount), 2) AS avg_spending
                FROM expenses
                GROUP BY day_of_week
                ORDER BY avg_spending DESC;
            """,

            "2. What is the average transaction value per category?": """
                SELECT category,
                       ROUND(AVG(amount), 2) AS avg_transaction_value
                FROM expenses
                GROUP BY category
                ORDER BY avg_transaction_value DESC;
            """,

            "3. Which categories have the highest spending variability?": """
                SELECT category,
                       ROUND(AVG(amount * amount) - AVG(amount) * AVG(amount), 2) AS variance
                FROM expenses
                GROUP BY category
                ORDER BY variance DESC;
            """,

            "4. What percentage of transactions are Cash vs Online?": """
                SELECT payment_mode,
                       COUNT(*) AS transaction_count,
                       ROUND(COUNT(*) * 100.0 /
                            (SELECT COUNT(*) FROM expenses), 2) AS percentage
                FROM expenses
                GROUP BY payment_mode;
            """,

            "5. What is the median expense amount per category?": """
                WITH ranked AS (
                    SELECT category,
                           amount,
                           ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount) AS rn,
                           COUNT(*) OVER (PARTITION BY category) AS cnt
                    FROM expenses
                )
                SELECT category,
                       ROUND(AVG(amount), 2) AS median_amount
                FROM ranked
                WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
                GROUP BY category;
            """,

            "6. Which week of the month contributes most to spending?": """
                SELECT ((CAST(strftime('%d', date) AS INTEGER) - 1) / 7 + 1) AS week_of_month,
                       ROUND(SUM(amount), 2) AS total_spent
                FROM expenses
                GROUP BY week_of_month
                ORDER BY total_spent DESC;
            """,

            "7. Month-over-month spending change": """
                WITH monthly AS (
                    SELECT SUBSTR(date,1,7) AS month,
                           SUM(amount) AS total_spent
                    FROM expenses
                    GROUP BY month
                )
                SELECT month,
                       total_spent,
                       total_spent - LAG(total_spent) OVER (ORDER BY month) AS change_amount
                FROM monthly;
            """,

            "8. Months with abnormal spending spikes": """
                WITH monthly AS (
                    SELECT SUBSTR(date,1,7) AS month,
                           SUM(amount) AS total_spent
                    FROM expenses
                    GROUP BY month
                )
                SELECT *
                FROM monthly
                WHERE total_spent > (SELECT AVG(total_spent) FROM monthly)
                ORDER BY total_spent DESC;
            """,

            "9. Categories showing seasonal behavior": """
                SELECT category,
                       ROUND(AVG(amount * amount) - AVG(amount) * AVG(amount), 2) AS variance
                FROM expenses
                GROUP BY category
                ORDER BY variance DESC;
            """,

            "10. Rolling 3-month average spending": """
                WITH monthly AS (
                    SELECT SUBSTR(date,1,7) AS month,
                           SUM(amount) AS total_spent
                    FROM expenses
                    GROUP BY month
                )
                SELECT month,
                       total_spent,
                       ROUND(AVG(total_spent) OVER (
                           ORDER BY month
                           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                       ), 2) AS rolling_avg
                FROM monthly;
            """,

            "11. Highest cashback-to-spend ratio by category": """
                SELECT category,
                       ROUND(SUM(cashback) * 100.0 / SUM(amount), 2) AS cashback_ratio
                FROM expenses
                WHERE cashback > 0
                GROUP BY category
                ORDER BY cashback_ratio DESC;
            """,

            "12. Cashback efficiency by payment mode": """
                SELECT payment_mode,
                       ROUND(SUM(cashback) * 100.0 / SUM(amount), 2) AS cashback_efficiency
                FROM expenses
                GROUP BY payment_mode
                ORDER BY cashback_efficiency DESC;
            """,

            "13. Percentage of spending with zero cashback": """
                SELECT ROUND(
                    SUM(CASE WHEN cashback = 0 THEN amount ELSE 0 END) * 100.0 /
                    SUM(amount), 2
                ) AS zero_cashback_percentage
                FROM expenses;
            """,

            "14. Transactions with cashback > 5%": """
                SELECT date, category, amount, cashback,
                       ROUND(cashback * 100.0 / amount, 2) AS cashback_percentage
                FROM expenses
                WHERE cashback * 1.0 / amount > 0.05
                ORDER BY cashback_percentage DESC;
            """,

            "15. Categories exceeding their monthly average": """
                WITH monthly_cat AS (
                    SELECT SUBSTR(date,1,7) AS month,
                           category,
                           SUM(amount) AS total_spent
                    FROM expenses
                    GROUP BY month, category
                ),
                avg_cat AS (
                    SELECT category,
                           AVG(total_spent) AS avg_spent
                    FROM monthly_cat
                    GROUP BY category
                )
                SELECT m.month, m.category, m.total_spent
                FROM monthly_cat m
                JOIN avg_cat a
                ON m.category = a.category
                WHERE m.total_spent > a.avg_spent
                ORDER BY m.month, m.total_spent DESC;
            """
        }

        selected_query = st.selectbox(
            "Select a self-created SQL query:",
            list(queries.keys()),
            key="query_selector_tab3"
        )

        if st.button("Run Query", key="run_query_tab3"):
            result = pd.read_sql_query(queries[selected_query], conn)
            st.dataframe(result, use_container_width=True)

        conn.close()


        
# ---------------- TAB 4 — ADD EXPENSE ----------------
with tab4:
    st.header("➕ Add New Expense")
    date = st.date_input("Date")
    category = st.text_input("Category")
    payment = st.selectbox("Payment Mode", ["Cash", "Online"])
    desc = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0)
    cashback = st.number_input("Cashback", min_value=0.0)

    if st.button("Add Expense"):
        insert_expense(str(date), category, payment, desc, amount, cashback)
        st.success("Expense added successfully!")


# ---------------- TAB 5 — RAW DATA ----------------
with tab5:
    st.header("📄 Raw Expense Data")
    if df.empty:
        st.warning("No expense data available.")
    else:
        st.dataframe(df, use_container_width=True)


# ---------------- TAB 6 — DOWNLOAD ----------------
with tab6:
    st.header("⬇️ Download Your Data")
    if df.empty:
        st.warning("Nothing to download.")
    else:
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "expenses.csv", "text/csv")
