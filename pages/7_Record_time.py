import streamlit as st
from lunch_menu.db import select_members_without_lunch

st.set_page_config(page_title="Record time", page_icon="⏱️")

st.markdown("# ⏱️ Record time")
st.sidebar.header("Record time")

# 데이터 조회 함수
def load_data():
    return select_members_without_lunch()

# 초기 데이터 조회
select_df = load_data()

# 버튼 UI
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 다시 조회"):
        select_df = load_data()

with col2:
    if st.button("📢 미작성자 알람 발송"):
        st.success("알람이 발송되었습니다!")  # 여기에 실제 알람 발송 기능 추가

# 데이터프레임 표시
if select_df.empty:
    st.info("✅ 오늘 점심 메뉴를 미작성한 사람이 없습니다!")
else:
    st.dataframe(select_df, use_container_width=True)




