import streamlit as st

st.set_page_config(layout="wide", page_title="AI Source Manager")

# ---------------- STATE ----------------
if "urls" not in st.session_state:
    st.session_state.urls = []

if "chat" not in st.session_state:
    st.session_state.chat = []

if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True


# ---------------- CSS ----------------
st.markdown("""
<style>

html, body, .stApp {
    background: #e9f1fb;
    font-family: 'Inter', sans-serif;
}

/* ---------------- PANELS ---------------- */

/* LEFT PANEL */
.left-panel {
    background: linear-gradient(180deg, #c2d4e6, #b7cade);
    border-radius: 16px;
    height: 85vh;
    padding: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    backdrop-filter: blur(10px);
}

/* RIGHT PANEL */
.right-panel {
    background: linear-gradient(180deg, #e7f1fb, #eef6ff);
    border-radius: 16px;
    height: 85vh;
    padding: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    backdrop-filter: blur(10px);
}

/* HEADER SECTION */
.panel-header {
    padding: 22px;
    flex-shrink: 0;
}

/* SCROLLABLE BODY SECTION */
.panel-body {
    padding: 22px;
    flex-grow: 1;
    overflow-y: auto;
}

/* INPUT SECTION */
.panel-input {
    padding: 22px;
    flex-shrink: 0;
}

/* ---------------- CHAT BUBBLES ---------------- */
.chat-user {
    background: rgba(0,122,255,0.22);
    padding: 10px 14px;
    border-radius: 12px;
    width: fit-content;
    margin-bottom: 8px;
}
.chat-ai {
    background: rgba(0,0,0,0.12);
    padding: 10px 14px;
    border-radius: 12px;
    width: fit-content;
    margin-bottom: 8px;
}

/* ---------------- HAMBURGER ---------------- */
.st-hamburger button {
    background: rgba(255,255,255,0.8);
    border-radius: 999px;
    border: 1px solid rgba(0,0,0,0.1);
    padding: 4px 12px;
    font-size: 20px;
}

/* ---------------- SCROLLBAR ---------------- */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track {
    background: rgba(255,255,255,0.2);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb {
    background: rgba(120,120,120,0.35);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(120,120,120,0.55);
}

</style>
""", unsafe_allow_html=True)


# ---------------- HAMBURGER ----------------
top_left, _ = st.columns([0.07, 0.93])

with top_left:
    with st.container():
        st.markdown('<div class="st-hamburger">', unsafe_allow_html=True)
        if st.button("☰", key="toggle_sidebar"):
            st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.markdown("</div>", unsafe_allow_html=True)


st.write("")


# ---------------- LAYOUT ----------------
if st.session_state.sidebar_open:
    col_left, col_right = st.columns([1, 2], gap="large")
else:
    col_left, col_right = st.columns([0.0001, 3], gap="large")


# ---------------- LEFT PANEL (Sources) ----------------
with col_left:
    if st.session_state.sidebar_open:

        with st.container():
            st.markdown("""
            <div class='left-panel'>
                <div class='panel-header'>
                    <h2>🌐 Sources</h2>
                </div>

                <div class='panel-body'>
            """, unsafe_allow_html=True)

            # --- LISTA URL ---
            for i, u in enumerate(st.session_state.urls):
                c1, c2 = st.columns([0.85, 0.15])
                with c1:
                    st.markdown(f"- [{u}]({u})", unsafe_allow_html=True)
                with c2:
                    if st.button("❌", key=f"url_delete_{i}"):
                        st.session_state.urls.pop(i)
                        st.experimental_rerun()

            st.markdown("</div>", unsafe_allow_html=True)

            # --- INPUT NA DOLE PANELU ---
            st.markdown("<div class='panel-input'>", unsafe_allow_html=True)

            url = st.text_input("Dodaj URL", placeholder="https://example.com", key="url_input")

            if st.button("Dodaj URL ➕"):
                if url.strip():
                    st.session_state.urls.append(url)
                    st.experimental_rerun()

            st.markdown("</div></div>", unsafe_allow_html=True)


# ---------------- RIGHT PANEL (Chat) ----------------
with col_right:

    with st.container():
        st.markdown("""
        <div class='right-panel'>
            <div class='panel-header'>
                <h2>🤖 Chat z AI</h2>
            </div>

            <div class='panel-body'>
        """, unsafe_allow_html=True)

        # --- WIADOMOŚCI ---
        for who, msg in st.session_state.chat:
            bubble = "chat-user" if who == "user" else "chat-ai"
            st.markdown(f"<div class='{bubble}'>{msg}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # --- INPUT NA DOLE PANELU ---
        st.markdown("<div class='panel-input'>", unsafe_allow_html=True)

        user_msg = st.text_input("Twoja wiadomość:", placeholder="Zadaj pytanie o źródła...", key="chat_input")

        if st.button("Wyślij 💬"):
            if user_msg.strip():
                st.session_state.chat.append(("user", user_msg))
                st.session_state.chat.append(("ai", "Tu będzie odpowiedź LLM."))
                st.experimental_rerun()

        st.markdown("</div></div>", unsafe_allow_html=True)
