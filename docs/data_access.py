import mysql.connector
import json
import pandas as pd

def convert_data_to_list(data):
    if isinstance(data, str):
        data = json.loads(data)
    elif isinstance(data, pd.DataFrame):
        data = data.to_dict(orient='records')
    else:
        raise ValueError("Unsupported data type. Only JSON string or DataFrame is supported.")
    return data

def get_database_connection():

    db = mysql.connector.connect(
        host="your_host",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    return db

def add_data_to_mysql(data):
   
    data = convert_data_to_list(data)
    db = get_database_connection()
    cursor = db.cursor()
    sql = "INSERT INTO your_table (name, age, email) VALUES (%s, %s, %s)"

    try:
        for item in data:
            values = (item['name'], item['age'], item['email'])
            cursor.execute(sql, values)

        db.commit()

        print("Data added successfully!")
    except mysql.connector.Error as error:
        db.rollback()
        print(f"Error adding data to MySQL: {error}")
    finally:
        cursor.close()
        db.close()



