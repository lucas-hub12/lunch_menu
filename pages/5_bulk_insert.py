import streamlit as st
from lunch_menu.db import get_connection, insert_menu
import pandas as pd

members = { "TOM" : 1, "cho" : 2, "hyun" : 3, "JERRY" : 4, "SEO" : 5, "jiwon" : 6, "jacob" : 7, "heejin" : 8, "lucas" : 9, "nuni" : 10 }

st.set_page_config(page_title="👇 BULK INSERT", page_icon="👇")

st.markdown("# 👇 BULK INSERT")
st.sidebar.header("BULK INSERT")

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



