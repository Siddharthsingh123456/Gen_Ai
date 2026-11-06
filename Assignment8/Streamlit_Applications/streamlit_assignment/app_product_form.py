
import streamlit as st

st.title("Product Form")

with st.sidebar:
    product_name = st.text_input("Product Name")
    category = st.selectbox(
        "Category",
        ["Electronics", "Books", "Clothing", "Food", "Sports"]
    )
    price = st.number_input("Price", min_value=0.0)

    if st.button("Add Product"):
        st.success("Product Added Successfully")
        st.write("Name:", product_name)
        st.write("Category:", category)
        st.write("Price:", price)
