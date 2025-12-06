import streamlit as st

from tab1_sources import tab1_view
from tab2_facts import tab2_view
from tab3_analysis import tab3_view

st.title("Analiza źródeł")

tab1, tab2, tab3 = st.tabs(
    ["1. Źródła wymagające kompresji", "2. Streszczenie i fakty", "3. Analiza"]
)

with tab1:
    tab1_view()

with tab2:
    tab2_view()

with tab3:
    tab3_view()
