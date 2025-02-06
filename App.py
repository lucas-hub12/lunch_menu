import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import psycopg
import os
from dotenv import load_dotenv

members = { "TOM" : 1, "cho" : 2, "hyun" : 3, "JERRY" : 4, "SEO" : 5, "jiwon" : 6, "jacob" : 7, "heejin" : 8, "lucas" : 9, "nuni" : 10 }

# https://docs.streamlit.io/develop/concepts/connections/secrets-management
# DB_CONFIG = {
   # "dbname": "sunsindb",
   # "user": "sunsin",
   # "password": "mysecretpassword",
   # "host": "localhost",
   # "port": "5432",
#}
# 위 정보를 안보이게 하는 방법은 아래 참고

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

st.title(f"점심기록장{db_name}")

st.subheader("입력")
menu_name = st.text_input("메뉴 이름", placeholder="예: 김치찌개")
#member_name = st.text_input("먹은 사람", value = "lucas")
dt = st.date_input("점심 날짜")

member_name = st.selectbox(
    "먹은 사람",
    options = list(members.keys()),
    index = list(members.keys()).index('lucas')
    
)
member_id = members[member_name]

st.write("You selected:", member_name)

isPress = st.button("메뉴 저장")

if isPress:
    if menu_name and member_id and dt:
        if insert_menu(menu_name, member_id, dt):
           st.success("입력 성공")
        else: 
            st.error(f"입력 실패")
    else:
        st.warning(f"모든 값을 입력해주세요!")

st.subheader("확인")

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

# conn.commit() -> 여기서는 자동으로 됨
cursor.close()
conn.close()

df = pd.read_csv('note/lunch_menu.csv')

start_index= df.columns.get_loc('2025-01-07')
mdf = df.drop(columns=['gmail', 'github', 'domain', 'vercel', 'role'])
df_melt = mdf.melt(id_vars=['ename'], var_name='dt', value_name='menu_name')

melted_df = df_melt[~df_melt['menu_name'].isin(['-', 'x', '<결석>'])]

# selected_df = pd.DataFrame([[1,2,3],[4,5,6]], columns=['a','b','c'])
selected_df = pd.DataFrame(rows, columns=['menu_name', 'member_name','dt'])
selected_df

st.subheader("통계")

# 📌 6️⃣ 직원별 메뉴 선택 횟수 계산
gdf = selected_df.groupby('member_name')['menu_name'].count().reset_index()
gdf

# 📊 Matplotlib로 바 차트 그리기
# https://docs.streamlit.io/develop/api-reference/charts/st.pyplot
try: 
    fig, ax = plt.subplots()
    gdf.plot(x="member_name", y="menu_name", kind="bar", ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다.")
    print(f"Exception:{e}")

# TO DO
# CSV 로드해서 한번에 다 디비에 INSERT 하는거
st.subheader("벌크 인서트")
isPress = st.button("한방에 인서트")

if isPress:
    conn = get_connection()
    cursor = conn.cursor()
    for i in range(len(melted_df)):
        m_id = members[melted_df.iloc[i]['ename']]
        cursor.execute("INSERT INTO lunch_menu (menu_name, member_id, dt) VALUES (%s, %s, %s)",
                       (melted_df.iloc[i]['ename'],
                        m_id,
                        melted_df.iloc[i]['dt']))
    conn.commit()  # 변경사항 저장
    conn.close()  # 연결 닫기
    st.success(f"인서트 완료!!{isPress}")
else:
     st.warning(f"❌ 인서트 오류(데이터 중복)발생")

