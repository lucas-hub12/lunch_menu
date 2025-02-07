import streamlit as st
from lunch_menu.db import select_table

st.set_page_config(page_title="CHECK", page_icon="✅")

st.markdown("# ✅ CHECK DATA")
st.sidebar.header("CHECK DATA")

st.subheader("확인")
selected_df = select_table()
selected_df



