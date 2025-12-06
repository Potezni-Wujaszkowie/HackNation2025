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
                col1, col2, col3, col4 = st.columns([0.6, 0.2, 0.2, 0.2])

                with col1:
                    st.write(url)

                with col2:
                    new_weight = st.number_input(
                        "Waga",
                        min_value=0.0, max_value=100.0,
                        value=weight,
                        step=0.01,
                        key=f"tab1_weight_url_{i}"
                    )
                    if new_weight != weight:
                        st.session_state.tab1_urls[i][1] = new_weight
                with col3:
                    if st.button("Zapisz zmianę", key=f"tab1_save_url_{i}"):
                        st.session_state.tab1_urls[i][1] = new_weight
                        st.rerun()
                with col4:
                    if st.button("Usuń", key=f"tab1_del_url_{i}"):
                        st.session_state.tab1_urls.pop(i)
                        st.rerun()

    else:
        if "tab1_files" not in st.session_state:
            st.session_state.tab1_files = []

        uploaded_file = st.file_uploader("Dodaj plik (drag and drop)", accept_multiple_files=False, key="tab1_file_uploader")
        new_file_weight = st.number_input(
            "Waga pliku",
            min_value=0.0, max_value=100.0,
            value=0.0,
            step=0.01,
            key="tab1_file_weight_input"
        )
        add_file_btn = st.button("+ Dodaj plik", key="tab1_add_file_btn", type="primary")

        if uploaded_file and add_file_btn:
            st.session_state.tab1_files.append([uploaded_file.name, new_file_weight])
            st.success(f"Dodano: {uploaded_file.name}")
            st.rerun()

        st.markdown("---")
        st.subheader("Dodane pliki")
        if not st.session_state.tab1_files:
            st.info("Nie ma jeszcze dodanych plików.")
        else:
            for i, (fname, weight) in enumerate(st.session_state.tab1_files):
                col1, col2, col3, col4 = st.columns([0.6, 0.2, 0.2, 0.2])
                with col1:
                    st.write(fname)
                with col2:
                    new_weight = st.number_input(
                        "Waga",
                        min_value=0.0, max_value=100.0,
                        value=weight,
                        step=0.01,
                        key=f"tab1_weight_file_{i}"
                    )
                with col3:
                    if st.button("Zapisz zmianę", key=f"tab1_save_file_{i}"):
                        st.session_state.tab1_files[i][1] = new_weight
                        st.rerun()
                with col4:
                    if st.button("Usuń", key=f"tab1_del_file_{i}"):
                        st.session_state.tab1_files.pop(i)
                        st.rerun()
