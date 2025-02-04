import streamlit as st
import pandas as pd

st.write("""
# LUCAS.STORE
Hello *lucas!*

![img](https://blog.kakaocdn.net/dn/0mySg/btqCUccOGVk/nQ68nZiNKoIEGNJkooELF1/img.jpg)
""")

df = pd.read_csv('note/lunch_menu.csv')
df[['ename', '2025-01-07']]

