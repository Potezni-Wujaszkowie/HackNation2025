import streamlit as st
import sys
import subprocess
import os
from tab1_sources import tab1_view
from tab2_facts import tab2_view
from tab3_analysis import tab3_view

def main():
    st.title("Cyfrowy Wieszcz")

    tab1, tab2, tab3 = st.tabs(
        ["1. Źródła", "2. Fakty i założenia", "3. Przewidywania i analiza"]
    )

    with tab1:
        tab1_view()

    with tab2:
        tab2_view()

    with tab3:
        tab3_view()


    
if __name__ == "__main__":
    main()