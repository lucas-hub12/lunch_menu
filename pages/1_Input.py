import streamlit as st
from lunch_menu.db import insert_menu
st.set_page_config(page_title="INPUT", page_icon="🧐")

st.markdown("# 🧐 INPUT Menu")
st.sidebar.header("INPUT Menu")

# TODO - 메뉴 입력하기 부분 코드 이동시키기

members = { "TOM" : 1, "cho" : 2, "hyun" : 3, "JERRY" : 4, "SEO" : 5, "jiwon" : 6, "jacob" : 7, "heejin" : 8, "lucas" : 9, "nuni" : 10 }

st.subheader("입력")
menu_name = st.text_input("메뉴 이름", placeholder="예: 김치찌개")
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






