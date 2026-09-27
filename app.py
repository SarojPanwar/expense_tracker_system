import streamlit as st
from database import add_expense,get_expenses,get_monthly_expenses, delete_expense
import pandas as pd

st.title("💰 Expense Tracker")
st.write("Track, manage, and analyze your daily expenses.")


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
    
    expenses = get_expenses()

    if expenses:
        df = pd.DataFrame(
            expenses,
            columns=["id", "date", "amount", "category", "description"]
        )

        # Convert amount from paise to rupees
        df["amount"] = df["amount"] / 100

        # Convert date to datetime
        df["date"] = pd.to_datetime(df["date"])

        # Current month
        current_date = pd.Timestamp.today()
        current_month = current_date.month
        current_year = current_date.year

        current_month_expenses = df[
            (df["date"].dt.month == current_month) &
            (df["date"].dt.year == current_year)
        ]

        total_spending = df["amount"].sum()
        monthly_spending = current_month_expenses["amount"].sum()
        transaction_count = len(df)
        average_expense = total_spending / transaction_count

        # Summary cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Spending", f"₹{total_spending:.2f}")

        with col2:
            st.metric("This Month", f"₹{monthly_spending:.2f}")

        with col3:
            st.metric("Transactions", transaction_count)

        with col4:
            st.metric("Average Expense", f"₹{average_expense:.2f}")

        # Recent expenses
        st.subheader("Recent Expenses")

        recent_expenses = df.sort_values(
            "date",
            ascending=False
        ).head(5)

        recent_expenses = recent_expenses[
            ["date", "amount", "category", "description"]
        ]

        recent_expenses["date"] = recent_expenses["date"].dt.strftime("%Y-%m-%d")
        recent_expenses["amount"] = recent_expenses["amount"].map(
            lambda x: f"₹{x:.2f}"
        )

        recent_expenses.columns = [
            "Date",
            "Amount",
            "Category",
            "Description"
        ]

        st.dataframe(
            recent_expenses,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No expenses recorded yet.")

# Add Expense
with add_tab:
    st.header("Add New Expense")
    if "add_message" not in st.session_state:
        st.session_state.add_message = None

    if st.session_state.add_message:
        st.success(st.session_state.add_message)
        st.session_state.add_message = None

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
        st.session_state.add_message = "Expense added successfully!"
        st.rerun()
        
# History
with history_tab:
    st.header("Expense History")
    st.write("Your recorded expenses will apear here.")
    
    expenses = get_expenses()
    if "delete_message" not in st.session_state:
        st.session_state.delete_message = None
    if st.session_state.delete_message:
        st.success(st.session_state.delete_message)
        st.session_state.delete_message = None

    if expenses:
        data = []
        for expense in expenses:
            expense_id, date, amount ,category,description = expense
            data.append({
                "ID" : expense_id,
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
        st.subheader("Delete Expense")
        expense_ids = [expense[0] for expense in expenses]

        selected_id = st.selectbox(
            "SELECT Expense ID to Delete",
            expense_ids
        )
        if st.button("Delete Expense"):
            delete_expense(selected_id)
            st.session_state.delete_message=(f"Expense ID {selected_id} deleted successfully!")
            st.rerun()
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
    expenses = get_expenses()

    if expenses:
        df = pd.DataFrame(
            expenses,
            columns=["id","date","amount","category","description"]

        )

        # convert amount from paise to repuees
        df["amount"] = df["amount"]/100
        # convert date to datetime
        df["date"] = pd.to_datetime(df["date"])
        # create month column
        df["month"] = df["date"].dt.to_period("M").astype(str)

        # Monthly spending
        monthly_spending = (
            df.groupby("month")["amount"]
            .sum()
        )
        st.subheader("Monthly Spending Trend")
        st.bar_chart(monthly_spending)

        total_spending = df["amount"].sum()
        transaction_count = len(df)
        average_expense = total_spending / transaction_count
        col1, col2, col3 = st.columns(3)
       
        with col1:
            st.metric("Total Spending", f"₹{total_spending:.2f}")

        with col2:
            st.metric("Total Transactions", transaction_count)

        with col3:
            st.metric("Average Expense", f"₹{average_expense:.2f}")

    else:
        st.info("No expenses available for analytics.")
   