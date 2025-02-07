import streamlit as st
from lunch_menu.db import select_table
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 CHART", page_icon="📊")

st.markdown("# 📊 CHART")
st.sidebar.header("CHART")

st.subheader("차트")
# 📊 Matplotlib로 바 차트 그리기
# https://docs.streamlit.io/develop/api-reference/charts/st.pyplot
selected_df = select_table()
gdf = selected_df.groupby('member_name')['menu_name'].count().reset_index()

try:
    fig, ax = plt.subplots()
    gdf.plot(x="member_name", y="menu_name", kind="bar", ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다.")
    print(f"Exception:{e}")



