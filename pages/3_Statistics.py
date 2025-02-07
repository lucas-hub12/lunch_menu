import streamlit as st
from lunch_menu.db import select_table
import pandas as pd

st.set_page_config(page_title="📝 STATISTICS", page_icon="📝")

st.markdown("# 📝 STATISTICS")
st.sidebar.header("STATISTICS")

st.subheader("통계")

selected_df = select_table()
gdf = selected_df.groupby('member_name')['menu_name'].count().reset_index()
gdf




