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



read_file = SlackDataLoader("./anonymized")


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
    elif options == "Top Users":
        get_top_users(data)
    elif options == "Top Messages":
        top_message_count( )     
    # button_clicked = st.sidebar.button("Click Me")
    # button_clicked2 = st.sidebar.button("Click Me2")
    
    # if button_clicked:
    #     st.write("All data")
    #     reply_counts(data)

def get_sidebar():
    selected_option = st.sidebar.selectbox("Select an option", ["All Data", "Top Users", "Top Messages"])
    return selected_option

def get_data():
    data = read_file.slack_parser("./anonymized/all-week8/")
    return data


def get_top_users(data):
    sorted_df = data.sort_values('reply_users_count', ascending=False)

    # Get the top 10 rows with highest reply_users_count
    top_10_counts = sorted_df.head(10)[['msg_content', 'reply_users_count']]

    st.dataframe(top_10_counts)

def top_message_count():

    reactions = read_file.parse_slack_reaction('./anonymized/all-week8/','random')
    sorted_df = reactions.sort_values('reaction_count', ascending=False)
    top_10_reactions = sorted_df.head(20)
    st.dataframe(top_10_reactions[['reaction_name', 'reaction_count']])

def reply_counts(data):
   return  st.dataframe(data)
    
main()



