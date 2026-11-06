
import streamlit as st

st.title("Price Calculator")

price = st.number_input("Original Price", min_value=0.0)
discount = st.slider("Discount (%)", 0, 50, 10)

final_price = price - (price * discount / 100)

st.write("Original Price:", price)
st.write("Discount:", discount, "%")
st.write("Final Price:", final_price)

st.table([
    ["Before", price],
    ["After", final_price]
])
