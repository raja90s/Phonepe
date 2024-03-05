import streamlit as st
from streamlit_option_menu import option_menu

#Streamlit Part

st.set_page_config(layout= "wide")
st.title("Phonepe Data Visualization and Exploration")

with st.sidebar:
    select=option_menu("Main Menu",["Home","Data Exploration", "Top Charts"])
