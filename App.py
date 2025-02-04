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

st.subheader("확인")

query = "select menu_name,member_name,dt from lunch_menu order by dt desc"

conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()

# conn.commit() -> 여기서는 자동으로 됨
cursor.close()


# selected_df = pd.DataFrame([[1,2,3],[4,5,6]], columns=['a','b','c'])
selected_df = pd.DataFrame(rows, columns=['menu_name', 'member_name','dt'])
selected_df


# 📌 2️⃣ 데이터 가져오기
def load_data():
    conn = get_connection()
    query = "select menu_name,member_name,dt from lunch_menu order by dt desc"
    df = pd.read_sql(query, conn)  # SQL 실행 후 pandas DataFrame으로 변환
    conn.close()
    return df

# 📌 3️⃣ Streamlit UI 구성
st.subheader("통계")

# 📌 4️⃣ 데이터 로드
df = load_data()

# 📌 5️⃣ 불필요한 값 제거
not_na_df = df[~df['menu_name'].isin(['-', 'x', '<결석>'])]

# 📌 6️⃣ 직원별 메뉴 선택 횟수 계산
gdf = not_na_df.groupby('member_name')['menu_name'].count().reset_index()
gdf

# 📊 Matplotlib로 바 차트 그리기
# https://docs.streamlit.io/develop/api-reference/charts/st.pyplot
fig, ax = plt.subplots()
gdf.plot(x="member_name", y="menu_name", kind="bar", ax=ax)
st.pyplot(fig)

st.subheader("CSV 통계")
df = pd.read_csv('note/lunch_menu.csv')

start_idx = df.columns.get_loc('2025-01-07')
melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], 
                     var_name='dt', value_name='menu')

not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]
gdf = not_na_df.groupby('ename')['menu'].count().reset_index()
#gdf.plot(x="ename", y="menu", kind="bar")

gdf

# 📊 Matplotlib로 바 차트 그리기
# https://docs.streamlit.io/develop/api-reference/charts/st.pyplot
fig, ax = plt.subplots()
gdf.plot(x="ename", y="menu", kind="bar", ax=ax)
st.pyplot(fig)

# TO DO
# CSV 로드해서 한번에 다 디비에 INSERT 하는거
st.subheader("벌크 인서트")
isPress = st.button("한방에 인서트")

if isPress:
    try:    
        df = pd.read_csv('note/lunch_menu.csv')
        start_idx = df.columns.get_loc('2025-01-07')
        melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2],
                    var_name='dt', value_name='menu') 
        df = melted_df[['ename', 'dt', 'menu']]

        def insert_data(df):
             conn = get_connection()
             cursor = conn.cursor()
            # SQL INSERT 문 (파라미터 바인딩)
             sql = "INSERT INTO lunch_menu (member_name, dt, menu_name) VALUES (%s, %s, %s)"
            # 튜플 형태로 변환 후 executemany 사용
             data = list(df.itertuples(index=False, name=None))
             print("첫 5개 데이터:", data[:5])

             cursor.executemany(sql, data)  # 대량 데이터 삽입 최적화
             conn.commit()  # 변경사항 저장
             conn.close()  # 연결 닫기
             st.success(f"인서트 완료!!{isPress}")
        # 📌 5️⃣ 함수 실행하여 데이터 삽입
        insert_data(df)
    except Exception as e:
        st.warningr(f"❌ 인서트 오류 발생: {e}")
         

