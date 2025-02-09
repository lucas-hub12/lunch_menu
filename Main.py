import streamlit as st

st.set_page_config(page_title="Main",page_icon="👋",)

st.write("# 팀순신 점심 데이터 EDA 👋")

st.markdown(
    """
    ༼ つ ◕_◕ ༽つ🍰🍔🍱🥗🍜🍕🍣🥩
    
    - 팀순신의 점심 기록 데이터를 분석하고 시각화합니다.
    - **팀원들은 Input에서 매일 점심메뉴를 입력해주세요!**
    - **👈 Statistics와 chart에서 분석결과를 볼 수 있습니다!**
    
    ### 분석 내용
    - 팀원별 누적 기록 횟수
    - 점심 메뉴별 인기 순위 📊
    - 당일 메뉴 기록을 하지 않은 자 색출 🕵️‍♂️
    """
)
