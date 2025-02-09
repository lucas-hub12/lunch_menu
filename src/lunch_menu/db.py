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
    selected_df = selected_df.sort_values(by='dt', ascending=False)
    return selected_df


def rank_menu():
    conn = get_connection()

    query = """
            SELECT menu_name, COUNT(*) AS order_count
            FROM lunch_menu
            GROUP BY menu_name
            ORDER BY order_count DESC
            limit 5;
            """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def select_members_without_lunch():
    query = """
            select 
            m.id, 
            m.name,
            lm.menu_name,
            lm.dt,
            created_at AS inserted_time,
            CURRENT_DATE AT TIME ZONE 'Asia/Seoul' AS today_timestamp,
            DATE(CURRENT_DATE AT TIME ZONE 'Asia/Seoul') AS today_date
            FROM member m
            LEFT JOIN lunch_menu lm 
            ON m.id = lm.member_id 
            AND lm.dt = DATE(CURRENT_DATE AT TIME ZONE 'Asia/Seoul')
            """
 # with 구문을 사용하여 자동으로 연결 및 커서 닫기
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
             cursor.execute(query)
             rows = cursor.fetchall()
             selected_columns = [col.name for col in cursor.description]  # 컬럼 이름 가져오기
            
 # DataFrame 생성
    df = pd.DataFrame(rows, columns=selected_columns)
    return df





