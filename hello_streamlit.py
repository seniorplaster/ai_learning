import streamlit as st

st.title("My First Streamlit App")
st.write("If you can see this in a browser, it worked.")

name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}! Welcome to AI app development.")