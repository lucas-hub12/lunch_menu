import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lunch_menu.db import get_connection, db_name, insert_menu, select_table

members = { "TOM" : 1, "cho" : 2, "hyun" : 3, "JERRY" : 4, "SEO" : 5, "jiwon" : 6, "jacob" : 7, "heejin" : 8, "lucas" : 9, "nuni" : 10 }

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

# 오늘  점심 임력 안 한사람을 알 수 있는 버튼 만들기

isPress = st.button("오늘 점심 입력 안 한 사람은 누구?")
query = """
SELECT
	m.name,
	count(l.id) as ctid
FROM
	member m
	LEFT JOIN lunch_menu l
	ON l.member_id = m.id
	AND l.dt = CURRENT_DATE
GROUP BY
	m.id,
	m.name
HAVING
	count(l.id) = 0
ORDER BY
	ctid desc
;
"""

if isPress:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            st.write("모두 입력 했습니다")
        else:
            # 이름만 추출하여 리스트로 변환
            names = [row[0] for row in rows]
            # 리스트를 하나의 문자열로 결합
            names_str = ", ".join(names)
            st.success(f"범인 검거:  {names_str} 입니다.")

    except Exception as e:
        st.warning(f"조회 중 오류가 발생했습니다")
        print(f"Exception: {e}")



st.subheader("확인")
selected_df = select_table()
selected_df

st.subheader("통계")

gdf = selected_df.groupby('member_name')['menu_name'].count().reset_index()
gdf


st.subheader("차트")
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
    try:                                                 
        df = pd.read_csv('note/lunch_menu.csv')
        start_idx = df.columns.get_loc('2025-01-07')
        rdf= df.melt(id_vars=['ename'], value_vars=(df.columns[start_idx:-2]),var_name='dt', value_name='menu')
        not_na_rdf = rdf[~rdf['menu'].isin(['-','<결석>','x'])]
# TODO
# 벌크인서트 버튼이 눌리면  성공/실패 구분해서 완료 메시지 출력하기
        # 총 건수
        total_count = len(not_na_rdf)
        # 성공 건수 + 성공은 insert 하기
        success_count = 0
        for _, row in not_na_rdf.iterrows():
            m_id = members[row['ename']]
            if insert_menu(row['menu'], m_id, row['dt']):
                success_count += 1
        # 실패 건수
        fail_count = total_count - success_count

        if total_count == success_count:
            st.success(f"벌크인서트 성공: 총{total_count}건")
        else:
            st.error(f"총건 {total_count}건중 {fail_count}건 실패")
    except Exception as e:
        st.warning(f"조회 중 오류가 발생했습니다")
        print(f"Exception: {e}")


