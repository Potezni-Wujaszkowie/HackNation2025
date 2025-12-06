import streamlit as st
import pandas as pd

def tab1_view():
    chosen_option = st.radio(
        "Wybierz opcję dodawania:",
        ["Dodaj URL", "Dodaj plik"], 
        horizontal=True
    )

    if chosen_option == "Dodaj URL":
        if "tab1_urls" not in st.session_state:
            st.session_state.tab1_urls = []

        st.subheader("Dodaj nowy URL")
        new_tab1_url = st.text_input(
            "Nowy adres:",
            placeholder="https://przykladowa_strona.pl",
            key="tab1_new_url_input"
        )

        if st.button("+ Dodaj URL", key="tab1_add_url_btn", type="primary"):
            if new_tab1_url.strip():
                st.session_state.tab1_urls.append([new_tab1_url.strip(), 0.0])
                st.rerun()

        st.markdown("---")
        st.subheader("Dodane adresy URL")

        if not st.session_state.tab1_urls:
            st.info("Nie ma jeszcze adresów.")
        else:
            for i, (url, weight) in enumerate(st.session_state.tab1_urls):
                col1, col2, col3 = st.columns([0.6, 0.2, 0.2])

                with col1:
                    st.write(url)

                with col2:
                    new_weight = st.number_input(
                        "Waga",
                        min_value=0.0, max_value=100.0,
                        value=weight,
                        step=0.01,
                        key=f"tab1_weight_{i}"
                    )
                    if new_weight != weight:
                        st.session_state.tab1_urls[i][1] = new_weight

                with col3:
                    if st.button("Usuń", key=f"del_{i}"):
                        st.session_state.tab1_urls.pop(i)
                        st.rerun()

    else:
        uploaded_file = st.file_uploader("Dodaj plik", accept_multiple_files=False)
        if uploaded_file:
            st.success(f"Dodano: {uploaded_file.name}")
