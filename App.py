import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg

DB_CONFIG = {
    "dbname": "sunsindb",
    "user": "sunsin",
    "password": "mysecretpassword",
    "host": "localhost",
    "port": "5432",
}

def get_connection():
    return psycopg.connect(**DB_CONFIG)

st.title("팀순신 점심 기록장")
st.subheader("입력")
menu_name = st.text_input("메뉴 이름", placeholder="예: 김치찌개")
member_name = st.text_input("먹은 사람", value = "Lucas")
dt = st.date_input("점심 날짜")

isPress = st.button("메뉴 저장")

if isPress:
    if menu_name and member_name and dt:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO lunch_menu (menu_name, member_name, dt) VALUES (%s,%s,%s);",
                (menu_name, member_name, dt)
        )   
        conn.commit()
        cursor.close()
        st.success(f"{isPress}:{menu_name},{member_name},{dt}")
    else:
        st.warning(f"모든 값을 입력해주세요!")






df = pd.read_csv('note/lunch_menu.csv')

start_idx = df.columns.get_loc('2025-01-07')
melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], 
                     var_name='dt', value_name='menu')

not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
gdf = not_na_df.groupby('ename')['menu'].count().reset_index()
#gdf.plot(x="ename", y="menu", kind="bar")

# 📊 Matplotlib로 바 차트 그리기
fig, ax = plt.subplots()
gdf.plot(x="ename", y="menu", kind="bar", ax=ax)
st.pyplot(fig)



