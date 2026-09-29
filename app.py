import streamlit as st
import sys
import os
import uuid
import re
import pandas as pd
import textwrap

# ============================================================
# PROJECT PATH
# ============================================================

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "src"
    )
)

from generate import generate_answer
from history import (
    init_db,
    save_session,
    load_all_sessions,
    load_session,
    delete_session
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PlaceWise | Placement Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()


# ============================================================
# SAFE HTML RENDERER
# ============================================================

def render_html(markup):
    """Render custom HTML as HTML, never as a Markdown code block."""
    html = textwrap.dedent(markup).strip()
    # st.html is the safest renderer for custom UI markup in modern Streamlit.
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)


# ============================================================
# PREMIUM UI — ELECTRIC INDIGO / SOFT LILAC / PORCELAIN
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --indigo: #5146E5;
        --indigo-dark: #3730A3;
        --indigo-soft: #EEECFF;
        --lilac: #F6F4FF;
        --porcelain: #FBFAFF;
        --white: #FFFFFF;
        --ink: #201D3A;
        --muted: #77738D;
        --muted-2: #A19CB4;
        --border: #E8E4F5;
        --border-strong: #D8D2EE;
    }

    /* ========================================================
       GLOBAL
       ======================================================== */

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    html, body {
        background: var(--porcelain) !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 72% 15%, rgba(126, 110, 246, 0.055), transparent 27%),
            var(--porcelain) !important;
        color: var(--ink) !important;
    }

    .main {
        background: transparent !important;
    }

    .block-container {
        max-width: 1440px !important;
        padding: 2.9rem 2.6rem 7rem 2.6rem !important;
    }
    .block-container {
    max-width: 1440px !important;
    padding: 1.2rem 2.6rem 7rem 2.6rem !important;
    }
    footer, #MainMenu {
        visibility: hidden !important;
    }

    header[data-testid="stHeader"] {
    display: none !important;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid var(--border) !important;
        width: 292px !important;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.05rem 0.9rem 1rem 0.9rem !important;
    }

    .sidebar-brand {
        position: relative;
        overflow: hidden;
        background: linear-gradient(145deg, #F0EDFF 0%, #FAF9FF 72%) !important;
        border: 1px solid #DDD7FF !important;
        border-radius: 20px !important;
        padding: 1.05rem 1.05rem 1rem 1.05rem !important;
        margin: 0 0 1.2rem 0 !important;
        box-shadow: 0 10px 28px rgba(81, 70, 229, 0.075) !important;
    }

    .sidebar-brand::after {
        content: "";
        position: absolute;
        width: 110px;
        height: 110px;
        right: -45px;
        top: -55px;
        border-radius: 50%;
        background: rgba(81, 70, 229, 0.07);
    }

    .sidebar-brand-row {
        display: flex;
        align-items: center;
        gap: 9px;
        position: relative;
        z-index: 1;
    }

    .sidebar-logo {
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 11px;
        background: linear-gradient(145deg, #5146E5, #756BF2);
        box-shadow: 0 7px 16px rgba(81, 70, 229, 0.2);
        font-size: 1rem;
    }

    .sidebar-brand-title {
        color: var(--indigo) !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
    }

    .sidebar-brand-subtitle {
        color: #77738F !important;
        font-size: 0.58rem !important;
        font-weight: 800 !important;
        letter-spacing: 1.05px !important;
        margin: 0.38rem 0 0 43px !important;
        position: relative;
        z-index: 1;
    }

    .section-label {
        color: #A19CB4 !important;
        font-size: 0.62rem !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.25px !important;
        margin: 1.15rem 0 0.48rem 0.18rem !important;
    }

    div[data-testid="stSidebar"] .stButton {
        margin: 0 0 0.3rem 0 !important;
    }

    div[data-testid="stSidebar"] .stButton button {
        width: 100% !important;
        min-height: 42px !important;
        padding: 0.5rem 0.75rem !important;
        background: transparent !important;
        color: #5C5870 !important;
        border: 1px solid transparent !important;
        border-radius: 12px !important;
        font-size: 0.83rem !important;
        font-weight: 650 !important;
        box-shadow: none !important;
        transition: all 0.18s ease !important;
    }

    div[data-testid="stSidebar"] .stButton button:hover {
        background: #F3F0FF !important;
        color: var(--indigo) !important;
        border-color: #E5E0FF !important;
        transform: translateX(1px);
    }

    div[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #5146E5, #6258EA) !important;
        color: #FFFFFF !important;
        border-color: #5146E5 !important;
        box-shadow: 0 8px 20px rgba(81, 70, 229, 0.18) !important;
    }

    div[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4338CA, #5146E5) !important;
        color: #FFFFFF !important;
        border-color: #4338CA !important;
        transform: translateY(-1px);
    }

    div[data-testid="stSidebar"] .stButton button:focus {
        box-shadow: 0 0 0 3px rgba(81, 70, 229, 0.08) !important;
    }

    .sidebar-divider {
        height: 1px;
        background: var(--border);
        margin: 1.05rem 0 0.2rem 0;
    }

    .empty-history {
        padding: 0.7rem 0.65rem;
        color: #A19CB4;
        font-size: 0.72rem;
        line-height: 1.5;
        background: #FBFAFF;
        border: 1px dashed #E3DEF3;
        border-radius: 11px;
    }

    /* Recent chat row */
    div[data-testid="stSidebar"] [data-testid="column"] .stButton button {
        min-height: 37px !important;
        font-size: 0.75rem !important;
    }

    /* Dataset */
    .dataset-box {
        background: linear-gradient(145deg, #FFFFFF, #FAF9FF) !important;
        border: 1px solid var(--border) !important;
        border-radius: 15px !important;
        padding: 0.78rem 0.85rem !important;
        margin-bottom: 0.52rem !important;
        box-shadow: 0 4px 15px rgba(52, 43, 100, 0.025) !important;
    }

    .dataset-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
    }

    .dataset-number {
        color: var(--indigo) !important;
        font-size: 1.12rem !important;
        font-weight: 800 !important;
    }

    .dataset-badge {
        color: #5148D9;
        background: #F0EEFF;
        border: 1px solid #E1DCFF;
        border-radius: 999px;
        padding: 3px 7px;
        font-size: 0.55rem;
        font-weight: 800;
        letter-spacing: 0.3px;
    }

    .dataset-label {
        color: #9994AA !important;
        font-size: 0.57rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.85px !important;
        margin-top: 0.18rem !important;
    }

    .tech-stack {
        color: #A19CB4 !important;
        font-size: 0.62rem !important;
        text-align: center;
        margin-top: 0.65rem;
    }

    /* ========================================================
       MAIN HEADER
       ======================================================== */

    .main-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.35rem;
    padding-top: 0.5rem;
    }

    .main-brand {
        display: flex;
        align-items: center;
        gap: 9px;
    }
    
    
    .main-brand-icon {
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: linear-gradient(145deg, #5146E5, #746AF2);
        box-shadow: 0 8px 20px rgba(81, 70, 229, 0.18);
        font-size: 1.05rem;
    }

    .main-brand-name {
        color: #252143 !important;
        font-size: 1.72rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.85px !important;
    }

    .main-brand-name span {
        color: var(--indigo) !important;
    }

    .verified-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        margin-top: 0;
        padding: 6px 10px;
        border-radius: 999px;
        color: #5148D9;
        background: #F1EFFF;
        border: 1px solid #E1DCFF;
        font-size: 0.61rem;
        font-weight: 750;
        white-space: nowrap;
    }

    .main-subtitle {
        color: #7D788F !important;
        font-size: 0.79rem !important;
        margin: 0.22rem 0 0 47px !important;
    }

    .header-rule {
        height: 1px;
        background: linear-gradient(90deg, #E8E4F5, rgba(232, 228, 245, 0.25), transparent);
        margin: 1rem 0 0 0;
    }

    /* ========================================================
       WELCOME
       ======================================================== */

    .welcome-wrap {
    min-height: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem 0 2rem 0;
}
    .welcome-content {
        width: min(930px, 100%);
        text-align: center;
    }

    .welcome-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 10px;
        border-radius: 999px;
        color: #5B52D7;
        background: #F1EFFF;
        border: 1px solid #E1DCFF;
        font-size: 0.61rem;
        font-weight: 800;
        letter-spacing: 0.45px;
        margin-bottom: 1rem;
    }

    .welcome-icon {
        width: 68px;
        height: 68px;
        margin: 0 auto 1rem auto;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 21px;
        background: linear-gradient(145deg, #5146E5 0%, #776DF4 100%);
        box-shadow: 0 15px 32px rgba(81, 70, 229, 0.2);
        font-size: 1.75rem;
    }
    
    .welcome-heading {
    color: #252143;
    font-size: clamp(1.9rem, 2.8vw, 2.6rem);
    font-weight: 800;
    letter-spacing: -1.2px;
    line-height: 1.15;
    margin-bottom: 0.6rem;
    word-wrap: break-word;
    overflow-wrap: break-word;
    }

    .welcome-heading span {
        color: var(--indigo);
    }

    .welcome-text {
        color: #77738C;
        font-size: 1.02rem;
        line-height: 1.7;
        max-width: 650px;
        margin: 0 auto 1.8rem auto;
    }

    .quick-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.85rem;
        text-align: left;
        max-width: 930px;
        margin: 0 auto;
    }

    .quick-card {
        position: relative;
        overflow: hidden;
        min-height: 128px;
        background: rgba(255,255,255,0.94);
        border: 1px solid var(--border);
        border-radius: 17px;
        padding: 1rem 1.05rem;
        box-shadow: 0 8px 24px rgba(52, 43, 100, 0.035);
        transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
    }

    .quick-card:hover {
        transform: translateY(-2px);
        border-color: #D8D1F8;
        box-shadow: 0 13px 30px rgba(81, 70, 229, 0.07);
    }

    .quick-card::after {
        content: "";
        position: absolute;
        width: 70px;
        height: 70px;
        right: -34px;
        bottom: -35px;
        border-radius: 50%;
        background: rgba(81, 70, 229, 0.045);
    }

    .quick-icon-wrap {
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: #F0EEFF;
        margin-bottom: 0.65rem;
        font-size: 0.95rem;
    }

    .quick-title {
        color: #302B50;
        font-size: 0.79rem;
        font-weight: 750;
        margin-bottom: 0.28rem;
    }

    .quick-text {
        color: #89849A;
        font-size: 0.68rem;
        line-height: 1.55;
    }

    .try-wrap {
        margin-top: 1.35rem;
    }

    .try-label {
        color: #A19CB4;
        font-size: 0.63rem;
        font-weight: 750;
        margin-bottom: 0.45rem;
    }

    .try-query {
        display: inline-block;
        max-width: 100%;
        padding: 8px 12px;
        color: #666178;
        background: #FFFFFF;
        border: 1px solid var(--border);
        border-radius: 999px;
        font-size: 0.67rem;
        box-shadow: 0 4px 14px rgba(52, 43, 100, 0.025);
    }

    /* ========================================================
       CHAT
       ======================================================== */

    div[data-testid="stChatMessage"] {
        border-radius: 15px !important;
        margin-bottom: 0.6rem !important;
    }

    div[data-testid="stChatMessage"] p {
        font-size: 0.9rem !important;
        line-height: 1.68 !important;
    }

    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        color: #312D47 !important;
    }

    .source-text {
        color: #5148D9 !important;
        font-size: 0.68rem !important;
        background: #F0EEFF !important;
        border: 1px solid #E1DCFF !important;
        border-radius: 20px !important;
        padding: 4px 9px !important;
        display: inline-block !important;
        margin: 2px 4px 2px 0 !important;
    }

    /* ========================================================
       CHAT INPUT
       ======================================================== */

    div[data-testid="stBottom"] {
        background: linear-gradient(180deg, rgba(251,250,255,0), #FBFAFF 28%) !important;
        border-top: 0 !important;
        padding-top: 0.8rem !important;
    }

    div[data-testid="stBottomBlockContainer"] {
        background: transparent !important;
        max-width: 1120px !important;
    }

    div[data-testid="stChatInput"] {
        background: #FFFFFF !important;
        border: 1px solid #DAD5EF !important;
        border-radius: 17px !important;
        box-shadow: 0 10px 28px rgba(52, 43, 100, 0.09) !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #A69EF5 !important;
        box-shadow: 0 0 0 3px rgba(81, 70, 229, 0.08),
                    0 12px 30px rgba(52, 43, 100, 0.1) !important;
    }

    div[data-testid="stChatInput"] textarea {
        background: #FFFFFF !important;
        color: #292540 !important;
        border: none !important;
        border-radius: 17px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #A09BAE !important;
        opacity: 1 !important;
    }

    /* ========================================================
       INSIGHTS
       ======================================================== */

    div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        box-shadow: 0 6px 18px rgba(52, 43, 100, 0.035) !important;
    }

    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 900px) {
        .block-container {
            padding: 2.6rem 1.2rem 6rem 1.2rem !important;
        }

        .quick-grid {
            grid-template-columns: 1fr;
            max-width: 620px;
        }

        .welcome-wrap {
            min-height: 54vh;
        }

        .verified-badge {
            display: none;
        }
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 2.5rem 0.85rem 5rem 0.85rem !important;
        }

        .main-brand-name {
            font-size: 1.42rem !important;
        }

        .main-brand-icon {
            width: 34px;
            height: 34px;
        }

        .main-subtitle {
            margin-left: 43px !important;
            font-size: 0.72rem !important;
        }

        .welcome-heading {
            font-size: 1.8rem;
        }

        .welcome-text {
            font-size: 0.82rem;
        }

        .quick-card {
            min-height: auto;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)



# ============================================================
# SESSION STATE
# ============================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "view" not in st.session_state:
    st.session_state.view = "chat"


# ============================================================
# HELPERS
# ============================================================

def make_chat_title(question):
    title = re.sub(r"\s+", " ", question.strip())
    if len(title) > 32:
        title = title[:32].rstrip() + "..."
    return title


def start_new_chat():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.view = "chat"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-row">
                <div class="sidebar-logo">🎓</div>
                <div class="sidebar-brand-title">PlaceWise</div>
            </div>
            <div class="sidebar-brand-subtitle">PLACEMENT INTELLIGENCE ASSISTANT</div>
        </div>
        """
    )

    st.markdown(
        '<div class="section-label">Workspace</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "＋  New Chat",
        key="new_chat",
        use_container_width=True,
        type="primary"
    ):
        start_new_chat()
        st.rerun()

    if st.button(
        "💬  Chat",
        key="nav_chat",
        use_container_width=True
    ):
        st.session_state.view = "chat"
        st.rerun()

    if st.button(
        "📊  Insights",
        key="nav_insights",
        use_container_width=True
    ):
        st.session_state.view = "insights"
        st.rerun()

    st.markdown(
        '<div class="section-label">Recent Conversations</div>',
        unsafe_allow_html=True
    )

    sessions = load_all_sessions()

    if not sessions:
        render_html(
            '<div class="empty-history">Your recent placement questions will appear here.</div>'
        )
    else:
        for sid, title, created in sessions[:8]:
            col1, col2 = st.columns([5, 1], gap="small")

            with col1:
                if st.button(
                    f"💬  {title[:25]}",
                    key=f"load_{sid}",
                    use_container_width=True
                ):
                    st.session_state.session_id = sid
                    st.session_state.messages = load_session(sid)
                    st.session_state.view = "chat"
                    st.rerun()

            with col2:
                if st.button(
                    "×",
                    key=f"delete_{sid}"
                ):
                    delete_session(sid)
                    st.rerun()

    st.markdown(
        '<div class="section-label">Verified Dataset</div>',
        unsafe_allow_html=True
    )

    render_html(
        """
        <div class="dataset-box">
            <div class="dataset-top">
                <div class="dataset-number">5</div>
                <div class="dataset-badge">VERIFIED</div>
            </div>
            <div class="dataset-label">PLACEMENT REPORTS</div>
        </div>
        """
    )

    render_html(
        """
        <div class="dataset-box">
            <div class="dataset-number" style="font-size:0.98rem;">2018–19 → 2022–23</div>
            <div class="dataset-label">REPORT COVERAGE</div>
        </div>
        """
    )

    render_html('<div class="sidebar-divider"></div>')

    st.caption("RAG · LangChain · ChromaDB · Groq")


# ============================================================
# MAIN HEADER
# ============================================================

render_html(
    """
    <div class="main-header">
        <div>
            <div class="main-brand">
                <div class="main-brand-icon">🎓</div>
                <div class="main-brand-name">Place<span>Wise</span></div>
            </div>
            <div class="main-subtitle">
                Placement Intelligence Assistant · Ask your college placement reports in natural language.
            </div>
        </div>
        <div class="verified-badge">✦ Verified placement reports</div>
    </div>
    <div class="header-rule"></div>
    """
)


# ============================================================
# CHAT VIEW
# ============================================================

if st.session_state.view == "chat":

    if not st.session_state.messages:
        render_html(
            """
            <div class="welcome-wrap">
                <div class="welcome-content">

                    <div class="welcome-eyebrow">✦ ASK • EXPLORE • DISCOVER</div>

                    <div class="welcome-icon">🎓</div>

                    <div class="welcome-heading">
                        Welcome to <span>PlaceWise</span>
                    </div>

                    <div class="welcome-text">
                        Your AI-powered placement intelligence assistant.
                        Ask natural-language questions and discover answers from
                        verified college placement reports.
                    </div>

                    <div class="quick-grid">
                        <div class="quick-card">
                            <div class="quick-icon-wrap">🏢</div>
                            <div class="quick-title">Explore Companies</div>
                            <div class="quick-text">
                                Discover recruiters and companies that appeared in the placement reports.
                            </div>
                        </div>

                        <div class="quick-card">
                            <div class="quick-icon-wrap">📊</div>
                            <div class="quick-title">Compare Placement Data</div>
                            <div class="quick-text">
                                Understand offers, company activity and trends across reporting years.
                            </div>
                        </div>

                        <div class="quick-card">
                            <div class="quick-icon-wrap">🔎</div>
                            <div class="quick-title">Ask the Reports</div>
                            <div class="quick-text">
                                Get answers grounded in the placement documents available to PlaceWise.
                            </div>
                        </div>
                    </div>

                    <div class="try-wrap">
                        <div class="try-label">TRY ASKING</div>
                        <div class="try-query">Which companies offered the highest number of placements?</div>
                    </div>

                </div>
            </div>
            """
        )

    # Existing messages
    for msg in st.session_state.messages:
        avatar = "🎓" if msg["role"] == "assistant" else "🧑"

        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

            if msg.get("sources"):
                for source in msg["sources"]:
                    render_html(
                        f"""
                        <span class="source-text">📄 {source}</span>
                        """
                    )

    question = st.chat_input("Ask about placement data…")

    if question:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user", avatar="🧑"):
            st.markdown(question)

        with st.chat_message("assistant", avatar="🎓"):
            with st.spinner("Searching verified placement records…"):
                try:
                    answer, sources = generate_answer(question)
                    unique_sources = list(
                        dict.fromkeys(
                            s["source"]
                            for s in sources
                        )
                    )
                except Exception as e:
                    answer = "Something went wrong while processing your question."
                    unique_sources = []
                    st.error(str(e))

            st.markdown(answer)

            for source in unique_sources:
                render_html(
                    f"""
                    <span class="source-text">📄 {source}</span>
                    """
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": unique_sources
            }
        )

        title = make_chat_title(question)
        save_session(
            st.session_state.session_id,
            title,
            st.session_state.messages
        )

        st.rerun()


# ============================================================
# INSIGHTS VIEW
# ============================================================

elif st.session_state.view == "insights":

    if not os.path.exists("placement_data.csv"):
        st.info(
            "Run `python src/analytics.py` once to generate the dashboard data."
        )
    else:
        df = pd.read_csv("placement_data.csv")

        st.markdown("## Placement Insights")
        st.caption("A visual summary of the placement data available to PlaceWise.")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Offers",
            int(df["offers"].sum())
        )

        col2.metric(
            "Unique Companies",
            df["company"].nunique()
        )

        col3.metric(
            "Years Covered",
            df["year"].nunique()
        )

        st.markdown("### 🏢 Top Recruiters")

        top10 = (
            df.groupby("company")["offers"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        st.bar_chart(top10)

        st.markdown("### 📈 Offers by Year")

        yearly = df.groupby("year")["offers"].sum()
        st.bar_chart(yearly)

        st.markdown("### 🔎 Search Companies")

        search = st.text_input(
            "Search company name",
            placeholder="Example: Infosys",
            label_visibility="collapsed"
        )

        if search:
            filtered_df = df[
                df["company"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.dataframe(
                df.sort_values(
                    "offers",
                    ascending=False
                ).head(30),
                use_container_width=True,
                hide_index=True
            )
