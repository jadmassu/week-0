
import json
import pandas as pd
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def convert_data_to_list(data):
    if isinstance(data, str):
        data = json.loads(data)
    elif isinstance(data, pd.DataFrame):
        data = data.to_dict(orient='records')
    else:
        raise ValueError("Unsupported data type. Only JSON string or DataFrame is supported.")
    return data

def get_database_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="user",
            password="",
            database="network_analysis"
        )
        return db

    except mysql.connector.Error as error:
        print(f"Error connecting to the database: {error}")
        return None


def add_data_to_mysql(data):
   
    data = convert_data_to_list(data)
    db = get_database_connection()
    cursor = db.cursor()
    sql= """
        INSERT INTO SlackInformation (
            msg_type,
            user,
            msg_content,
            sender_name,
            msg_sent_time,
            msg_dist_type,
            time_thread_start,
            reply_count,
            reply_users_count,
            reply_users,
            tm_thread_end,
            channel
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """
        
    try:
        for item in data:
            values = (item['msg_type'], item['user'], item['msg_content'], item['sender_name'],item['msg_sent_time'],item['msg_dist_type'],
                      item['time_thread_start'],item['reply_count'],item['reply_users_count'],item['reply_users'],item['tm_thread_end'],
                      item['channel'])
            cursor.execute(sql, values)

        db.commit()

        print("Data added successfully!")
    except mysql.connector.Error as error:
        db.rollback()
        print(f"Error adding data to MySQL: {error}")
    finally:
        cursor.close()
        db.close()


def create_database(sql_file_path):
    try:
        db = get_database_connection()
        cursor = db.cursor()

        with open(sql_file_path, "r") as sql_file:
            sql_queries = sql_file.read().split(';')

        for sql_query in sql_queries:
            if sql_query.strip():
                cursor.execute(sql_query)
                # If there are result sets, fetch or clear them
                while cursor.nextset():
                    pass

        db.commit()

    except mysql.connector.Error as error:
        print(f"Error executing SQL query: {error}")

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'db' in locals() and db.is_connected():
            db.close()