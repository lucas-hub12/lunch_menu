import pandas as pd
import psycopg
from dotenv import load_dotenv
import os

# https://docs.streamlit.io/develop/concepts/connections/secrets-management
load_dotenv()

db_name = os.getenv("DB_NAME")

DB_CONFIG = {
    #"user": st.secrets["db_username"]
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

def get_connection():
    return psycopg.connect(**DB_CONFIG)

def insert_menu(menu_name, member_id, dt):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
                  "INSERT INTO lunch_menu (menu_name, member_id, dt) VALUES (%s,%s,%s);",
                  (menu_name, member_id, dt)
                      )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
           print(f"Exception:{e}:")
           return False

def select_table():
    query = """
            SELECT
            l.menu_name,
            m.name,
            l.dt
            FROM
            lunch_menu l
            inner join member m
            on l.member_id = m.id
         """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # selected_df = pd.DataFrame([[1,2,3],[4,5,6]], columns=['a','b','c'])
    selected_df = pd.DataFrame(rows, columns=['menu_name', 'member_name','dt'])
    return selected_df





