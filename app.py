import streamlit as st
from database import add_expense,get_expenses,get_monthly_expenses
import pandas as pd
st.title("💰 Expense Tracker")
st.write("Track, manage, and analyze your daily expenses.")
st.subheader("Add Expense")

# Navigation tabs
dashboard_tab, add_tab,history_tab,monthly_tab,analytics_tab = st.tabs(
    [
        "🏠 Dashboard",
        "➕ Add Expense",
        "📋 History",
        "📅 Monthly Report",
        "📊 Analytics"  
    ]
)

# Dashboard
with dashboard_tab:
    st.header("Dashboard")
    st.write("Your overall expense summary will apear here.")

# Add Expense
with add_tab:
    st.header("Add New Expense")
    
    expense_date= st.date_input("Date")
    amount = st.number_input(
        "Amount (₹)",
        min_value=0.01,
        step=0.01
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertaiment",
            "Health",
            "Education",
            "Other"
        ]
    )

    description = st.text_input("Description")

    if st.button("Add Expense"):
        amount_in_paise = round(amount*100)

        add_expense(
            str(expense_date),
            amount_in_paise,
            category,
            description
        )
        st.success("Expense added successfully!")
        
# History
with history_tab:
    st.header("Expense History")
    st.write("Your recorded expenses will apear here.")
    
    expenses = get_expenses()

    if expenses:
        data = []
        for expense in expenses:
            expense_id, date, amount ,category,description = expense
            data.append({
                "Date":date,
                "Amount":f"₹{amount / 100:.2f}",
                "Category": category,
                "Description":description
            })
            df = pd.DataFrame(data)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("No expenses recorded yet.")


# Monthly Report
with monthly_tab:
    st.header("Monthly Report")
    
    months = ["January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"]
       
    years =[2025, 2026,2027]

    selected_year = st.selectbox(
        "Select Year",
        years
    )
    selected_month = st.selectbox(
        "Selecet Month",
        months
    )

    # Convert month name to month number
    month_number = months.index(selected_month)+1

    # Create start date
    start_date = f"{selected_year}-{month_number:02d}-01"

    # Create end date
    if month_number ==12:
        end_Date = f"{selected_year+1}-01-01"
    else:
        end_date = f"{selected_year}-{month_number + 1:02d}-01"

    # Get expenses for selected month
    monthly_expenses = get_monthly_expenses(
        start_date,
        end_date
    )
    if monthly_expenses:
        # Convert database records info Dataframe
        df = pd.DataFrame(
            monthly_expenses,
            columns=[
                "id",
                "date",
                "amount",
                "category",
                "description"
            ]
        )
        # Calculate total spending
        total_amount = df["amount"].sum() /100
        # Calculate number of transactions
        transaction_count = len(df)
        # Calculate average expense
        average_amount = total_amount / transaction_count

        # Display metrics
        col1 , col2 ,col3 = st.columns(3)
        with col1:
            st.metric(
                "Total spending",
                f"₹{total_amount:.2f}"
            )
        with col2:
            st.metric(
                "Transactions",
                transaction_count

            )
        with col3 :
            st.metric(
                "Average Expense",
                f"₹{average_amount:.2f}"

            )

        # Category breakdown
        st.subheader("Category Breakdown")
        category_summary = (
        df.groupby("category")["amount"]
        .sum()
        .div(100)
        .reset_index()
         )

        category_summary.columns = [
            "Category",
            "Total Spending"
        ]

        category_summary["Total Spending"] = (
            category_summary["Total Spending"]
            .map(lambda x: f"₹{x:.2f}")
        )

        st.dataframe(
            category_summary,
            use_container_width=True,
            hide_index=True
        )
        st.subheader("Spending by Category")
        chart_data = (
            df.groupby("category")["amount"]
            .sum()
            .div(100)
        
        )
        st.bar_chart(chart_data)

    else:
        st.info(
             f"No expenses found for {selected_month} {selected_year}."
        )

# Analytics
with analytics_tab:
    st.header("Expense Analytics")
    st.write("Charts and spending analysis will apear here.")