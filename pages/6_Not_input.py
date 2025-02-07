import streamlit as st
from lunch_menu.db import get_connection, insert_menu
st.set_page_config(page_title="NOT INPUT", page_icon="❌")

st.markdown("# ❌ NOT INPUT")
st.sidebar.header("NOT INPUT")

members = { "TOM" : 1, "cho" : 2, "hyun" : 3, "JERRY" : 4, "SEO" : 5, "jiwon" : 6, "jacob" : 7, "heejin" : 8, "lucas" : 9, "nuni" : 10 }

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

        
