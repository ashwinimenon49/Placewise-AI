import streamlit as st
import sys, os, uuid
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from generate import generate_answer
from history import init_db, save_session, load_all_sessions, load_session, delete_session
import pandas as pd

st.set_page_config(page_title="PlaceWise", page_icon="🎓", layout="wide")
init_db()

# ============ PREMIUM STYLING ============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f1a 0%, #14141f 100%);
    border-right: 1px solid #24243a;
}

/* Brand card — elevated, glass effect */
.brand-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.08));
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 24px rgba(99,102,241,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
}
.brand-title {
    font-size: 1.5rem; font-weight: 800;
    background: linear-gradient(90deg, #a5b4fc, #f0abfc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.1rem;
}
.brand-subtitle { color: #8b8ba7; font-size: 0.78rem; font-weight: 500; letter-spacing: 0.3px; }

/* Section labels */
.nav-section-label {
    color: #6b6b8a; font-size: 0.7rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px;
    margin: 1.2rem 0 0.5rem 0.2rem;
}

/* Nav buttons — elevated cards */
div[data-testid="stSidebar"] .stButton button {
    background: #1a1a2e;
    color: #c7c7e0;
    border: 1px solid #262640;
    border-radius: 10px;
    text-align: left;
    padding: 0.55rem 0.9rem;
    font-weight: 500;
    font-size: 0.88rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    transition: all 0.2s ease;
}
div[data-testid="stSidebar"] .stButton button:hover {
    border-color: #8b5cf6;
    background: #22223a;
    box-shadow: 0 4px 14px rgba(139,92,246,0.25);
    transform: translateY(-1px);
}

/* Active nav indicator */
.nav-active button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.4) !important;
}

/* Stat cards — layered depth */
.stat-card {
    background: linear-gradient(145deg, #1c1c30, #14141f);
    border: 1px solid #2a2a45;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.7rem;
    box-shadow: 0 6px 16px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04);
}
.stat-number { font-size: 1.4rem; font-weight: 800; color: #a5b4fc; }
.stat-label { font-size: 0.68rem; color: #7a7a9a; text-transform: uppercase; letter-spacing: 0.6px; }

/* History items */
.history-card {
    background: #16162654;
    border: 1px solid #22223a;
    border-radius: 10px;
    padding: 0.1rem;
    margin-bottom: 0.3rem;
}

/* Main header */
.main-header-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(236,72,153,0.05));
    border: 1px solid #24243a;
    border-radius: 18px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}
.main-title { font-size: 2.1rem; font-weight: 800;
    background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.main-subtitle { color: #9494b0; font-size: 0.92rem; margin-top: 0.2rem; }

.source-badge {
    display: inline-block; background: linear-gradient(135deg, #1e1b4b, #312e81);
    color: #b4b4fc; padding: 5px 13px; border-radius: 20px; font-size: 0.72rem;
    margin: 3px 4px 0 0; border: 1px solid #4338ca;
    box-shadow: 0 2px 8px rgba(67,56,202,0.3);
}

.coverage-number {
    font-size: 1.15rem;
    font-weight: 800;
    color: #a5b4fc;
    white-space: nowrap;
}

footer {visibility: hidden;} #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE ============
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "view" not in st.session_state:
    st.session_state.view = "chat"

# ============ SIDEBAR ============
with st.sidebar:
    # 1. BRAND
    st.markdown("""
    <div class="brand-card">
        <div class="brand-title">🎓 PlaceWise</div>
        <div class="brand-subtitle">PLACEMENT ASSISTANT AI</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. NAVIGATION
    st.markdown('<div class="nav-section-label">Navigate</div>', unsafe_allow_html=True)

    nav_items = [("💬", "Chat", "chat"), ("📊", "Insights", "insights")]
    for icon, label, key in nav_items:
        active = st.session_state.view == key
        wrapper_class = "nav-active" if active else ""
        st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.view = key
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("➕  New Chat", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.view = "chat"
        st.rerun()

    # 3. HISTORY
    st.markdown('<div class="nav-section-label">Recent Conversations</div>', unsafe_allow_html=True)
    sessions = load_all_sessions()
    if not sessions:
        st.caption("No saved chats yet.")
    for sid, title, created in sessions[:8]:
        col1, col2 = st.columns([5, 1])
        with col1:
            if st.button(f"💬 {title[:26]}", key=f"load_{sid}", use_container_width=True):
                st.session_state.session_id = sid
                st.session_state.messages = load_session(sid)
                st.session_state.view = "chat"
                st.rerun()
        with col2:
            if st.button("🗑️", key=f"del_{sid}"):
                delete_session(sid)
                st.rerun()

    # 4. STATS
    st.markdown('<div class="nav-section-label">Dataset</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="stat-card">
    <div class="stat-number">5</div>
    <div class="stat-label">PLACEMENT REPORTS</div>
</div>

<div class="stat-card">
    <div class="coverage-number">2018–19 to 2022–23</div>
    <div class="stat-label">REPORT COVERAGE</div>
</div>
""", unsafe_allow_html=True)

    
    st.markdown("---")
    st.caption("Built with RAG · LangChain · ChromaDB · Groq")

# ============ MAIN AREA HEADER ============
st.markdown("""
<div class="main-header-card">
    <div class="main-title">🎓 PlaceWise</div>
    <div class="main-subtitle">Ask anything about placement records — powered by AI, grounded in official college data</div>
</div>
""", unsafe_allow_html=True)

# ============ VIEW: CHAT ============
if st.session_state.view == "chat":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🎓" if msg["role"] == "assistant" else "🧑"):
            st.markdown(msg["content"])
            if msg.get("sources"):
                badges = "".join([f'<span class="source-badge">📄 {s}</span>' for s in msg["sources"]])
                st.markdown(badges, unsafe_allow_html=True)

    question = st.chat_input("Ask about placement data...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(question)

        with st.chat_message("assistant", avatar="🎓"):
            with st.spinner("Searching placement records..."):
                try:
                    answer, sources = generate_answer(question)
                    unique_sources = list(dict.fromkeys(s["source"] for s in sources))
                except Exception as e:
                    answer, unique_sources = f"Something went wrong: {e}", []
            st.markdown(answer)
            if unique_sources:
                badges = "".join([f'<span class="source-badge">📄 {s}</span>' for s in unique_sources])
                st.markdown(badges, unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": answer, "sources": unique_sources})
        title = st.session_state.messages[0]["content"]
        save_session(st.session_state.session_id, title, st.session_state.messages)
        st.rerun()
# ============ VIEW: INSIGHTS ============
elif st.session_state.view == "insights":
    if not os.path.exists("placement_data.csv"):
        st.info("Run `python src/analytics.py` once to generate the dashboard data.")
    else:
        df = pd.read_csv("placement_data.csv")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Offers", int(df["offers"].sum()))
        col2.metric("Unique Companies", df["company"].nunique())
        col3.metric("Years Covered", df["year"].nunique())

        st.markdown("#### 🏆 Top 10 Recruiters")
        top10 = df.groupby("company")["offers"].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top10)

        st.markdown("#### 📈 Offers by Year")
        yearly = df.groupby("year")["offers"].sum()
        st.bar_chart(yearly)

        st.markdown("#### 🔍 Search Companies")
        search = st.text_input("Filter by name")
        if search:
            st.dataframe(df[df["company"].str.contains(search, case=False, na=False)])
        else:
            st.dataframe(df.sort_values("offers", ascending=False).head(30))