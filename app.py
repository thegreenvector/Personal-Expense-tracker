import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database import add_transaction, get_transactions

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

st.title("Personal Expense Tracker")
st.write("Track income, expenses, savings, and spending patterns.")

st.subheader("Add Transaction")

with st.form("transaction_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        transaction_date = st.date_input("Date", date.today())
        transaction_type = st.selectbox("Type", ["Expense", "Income"])
        amount = st.number_input("Amount", min_value=0.01, value=100.0)

    with col2:
        category = st.selectbox(
            "Category",
            ["Food", "Transport", "Shopping", "Rent", "Entertainment",
             "Salary", "Freelance", "Health", "Education", "Other"]
        )
        description = st.text_input("Description")

    submitted = st.form_submit_button("Add Transaction", type="primary")

    if submitted:
        add_transaction(
            str(transaction_date),
            transaction_type,
            category,
            amount,
            description
        )
        st.success("Transaction added successfully!")

rows = get_transactions()

if rows:
    df = pd.DataFrame(
        rows,
        columns=["ID", "Date", "Type", "Category", "Amount", "Description"]
    )

    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    income = df.loc[df["Type"] == "Income", "Amount"].sum()
    expenses = df.loc[df["Type"] == "Expense", "Amount"].sum()
    balance = income - expenses

    st.divider()
    st.subheader("Financial Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"{income:,.2f}")
    col2.metric("Total Expenses", f"{expenses:,.2f}")
    col3.metric("Balance", f"{balance:,.2f}")

    st.divider()
    st.subheader("Spending Analytics")

    expense_df = df[df["Type"] == "Expense"]

    if not expense_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.pie(
                expense_df,
                names="Category",
                values="Amount",
                title="Expenses by Category"
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            monthly = expense_df.groupby("Month", as_index=False)["Amount"].sum()
            fig2 = px.bar(
                monthly,
                x="Month",
                y="Amount",
                title="Monthly Expenses"
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Transaction History")

    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False)
    st.download_button(
        "Download CSV Report",
        csv,
        "expense_report.csv",
        "text/csv"
    )

else:
    st.info("No transactions yet. Add your first transaction above!")
