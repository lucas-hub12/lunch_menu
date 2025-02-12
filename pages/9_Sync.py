import streamlit as st
import datetime
import pandas as pd
import requests
import lunch_menu.constants as const

st.set_page_config(page_title="SYNC", page_icon="🔄")

st.markdown("# 🔄 SYNC")
st.sidebar.header("모두의 점심 데이터 비교 합치기")
EP = "https://raw.githubusercontent.com/lucas-hub12/nextjs-fastapi-starter/refs/heads/main/endpoints.json"
res = requests.get(EP)
data = res.json()
endpoints = data['endpoints']

for p in endpoints:
    print(f'{p["name"]},{p["url"]}')

if st.button("데이터 동기화 하기"):
    lucas_url = "https://ac.lucas12.store/api/py/select_all"
    lucas_df = pd.DataFrame(requests.get(lucas_url).json())
    # 새로운 데이터 저장할 리스트
    new_data = []
    new_sources = 0

    for endpoint in endpoints:
        response = requests.get(endpoint["url"])
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            # lucas_df와 비교하여 없는 데이터 찾기
            diff_df = df[~df.isin(lucas_df.to_dict(orient='list')).all(axis=1)]
            if not diff_df.empty:
                new_data.append(diff_df)
                new_sources += 1
        else:
            print(f"{endpoint['name']}에서 데이터 가져오기 실패")

    # 새로운 데이터프레임 만들기
    if new_data:
        final_df = pd.concat(new_data, ignore_index=True)
        new_count = len(final_df)
        print("새로운 데이터:")
        print(final_df)
        
        # 성공 메시지 출력
        st.success(f"작업완료 - 새로운 원천 {new_sources} 곳에서 총 {new_count} 건을 새로 추가 하였습니다.")
        
        st.subheader("📊 새롭게 추가된 데이터")
        st.dataframe(final_df)
    else:
        print("새로운 데이터가 없습니다.")
        st.warning("새로운 데이터가 없습니다.")
    # API 목록 갖고 오기
    # 그 중 내것을 빼고
    # 목록을 순회하면서 나의 df 랑 비교해서 없는 것 => 데이터프레임 만들고
    # 데이터 프레임을 순회하면서 insert 한다.





    
