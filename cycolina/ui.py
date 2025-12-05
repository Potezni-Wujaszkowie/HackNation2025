import streamlit as st

st.set_page_config(page_title="AI Source Manager", layout="wide")

# -------------------- CSS FOR COLORS --------------------
st.markdown("""
<style>
/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #cfe8ff !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------- STATE --------------------
if "urls" not in st.session_state:
    st.session_state.urls = []


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.title("Sources")

    st.subheader("Dodaj nowy URL")
    new_url = st.text_input(
        "Nowy adres:", 
        placeholder="https://example.com",
        key="new_url_input"
    )

    if st.button("+ Dodaj URL", type="primary"):
        if new_url.strip():
            st.session_state.urls.append(new_url.strip())
            st.rerun()

    st.markdown("---")
    st.subheader("Dodane adresy URL")

    if not st.session_state.urls:
        st.info("Brak adresów. Dodaj pierwszy URL powyżej.")
    else:
        for i, url in enumerate(st.session_state.urls):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(url)
            with col2:
                if st.button("X", key=f"del_{i}"):
                    st.session_state.urls.pop(i)
                    st.rerun()


# -------------------- MAIN SCREEN --------------------
st.markdown("## Analiza źródeł")

st.write("Dodaj adresy URL w panelu po lewej, a następnie rozpocznij analizę poniżej:")

if st.button("Przeanalizuj źródła", type="primary", use_container_width=True):
    if not st.session_state.urls:
        st.warning("Najpierw dodaj URL-e w panelu po lewej.")
    else:
        st.success(f"Analizuję {len(st.session_state.urls)} źródeł... (tu będzie logika analizy)")
