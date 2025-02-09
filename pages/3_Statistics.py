import streamlit as st
from lunch_menu.db import get_connection, select_table 
import pandas as pd
import psycopg

st.set_page_config(page_title="📝 STATISTICS", page_icon="📝")

st.markdown("# 📝 STATISTICS")
st.sidebar.header("STATISTICS")

st.subheader("통계")

st.markdown("""**누적 기록자 통계**""")

selected_df = select_table()
gdf = selected_df.groupby('member_name')['menu_name'].count().reset_index()
gdf = gdf.sort_values(by='menu_name', ascending=False)
gdf

st.markdown(""" **점심 메뉴별 인기 순위 📊**""")
conn = get_connection()

query ="""
        SELECT RANK() OVER (ORDER BY COUNT(*) DESC) AS rank, menu_name, COUNT(*) AS order_count
        FROM lunch_menu
        GROUP BY menu_name
        ORDER BY order_count DESC
        limit 5;
       """
df = pd.read_sql(query, conn)
conn.close()
df
