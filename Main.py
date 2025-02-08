import streamlit as st

st.set_page_config(page_title="Main",page_icon="👋",)

st.write("# 팀순신 점심 데이터 EDA 👋")

st.markdown(
    """
    ༼ つ ◕_◕ ༽つ🍰🍔🍱🥗🍜🍕🍣🥩
    
    - 팀순신의 점심 기록 데이터를 분석하고 시각화합니다.
    - **👈 사이드바에서 원하는 분석 항목을 선택하세요!**
    
    ### 분석 내용
    - 점심 메뉴별 인기 순위 📊
    - 요일별 선호 음식 🍽️
    - 점심 비용 분포 💰
    - 특정 메뉴에 대한 트렌드 분석 📈
    - 기록 하지 않은 자 색출 🕵️‍♂️
    """
)
