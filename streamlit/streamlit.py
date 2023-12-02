import streamlit as st

def main():
    st.set_page_config(page_title="Slack Report", layout="wide")
    
    col_left, col_right = st.columns((1, 1))
    col_left.title("Slack Report")
    col_left.write("analysis report")
    

main()