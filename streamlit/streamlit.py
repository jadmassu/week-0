import streamlit as st
import os, sys
# Add parent directory to path to import modules from src
rpath = os.path.realpath('src')
print(rpath)
if rpath not in sys.path:
    sys.path.insert(0, rpath)

print(sys.path)
from loader import SlackDataLoader
import utils as utils



read_file = SlackDataLoader("../anonymized")


def main():
    st.set_page_config(page_title="Slack Report", layout="wide")
    
    col_left, col_right = st.columns((1, 1))
    col_left.title("Slack Report")
    col_left.write("analysis report")
    st.sidebar.title("Sidebar ")
    options = get_sidebar()
    data = get_data()
  
    if options == "All Data":
      
        reply_counts(data)
    # button_clicked = st.sidebar.button("Click Me")
    # button_clicked2 = st.sidebar.button("Click Me2")
    
    # if button_clicked:
    #     st.write("All data")
    #     reply_counts(data)

def get_sidebar():
    selected_option = st.sidebar.selectbox("Select an option", ["All Data", "Option 2", "Option 3"])
    return selected_option

def get_data():
    data = read_file.slack_parser("../anonymized/all-week8/")
    return data


def reply_counts(data):
   return  st.dataframe(data)
    
main()



