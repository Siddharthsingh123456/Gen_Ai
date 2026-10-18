
import streamlit as st

st.title("Sales Dashboard")

months = ["January", "February", "March", "April"]

sales = {
    "January": 1200,
    "February": 1500,
    "March": 900,
    "April": 2000
}

selected_month = st.selectbox("Select Month", months)

st.write("Month:", selected_month)
st.write("Sales:", sales[selected_month])

st.bar_chart(list(sales.values()))
