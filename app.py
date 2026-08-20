import streamlit as st
import os
from dotenv import load_dotenv

import config
from utils import data_loading
from tabs import (
    tab_preview,
    tab_profile,
    tab_cleaning,
    tab_stats,
    tab_correlations,
    tab_visualizations,
    tab_ai_insights,
    tab_forecasting,
    tab_final_report
)

# ============================================================
# LOAD ENVIRONMENT
# ============================================================
load_dotenv()

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Universal.DA | AI Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 🎨 PREMIUM DARK AI THEME
# ============================================================
st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 5%, rgba(6, 182, 212, 0.10), transparent 25%),
            radial-gradient(circle at 90% 10%, rgba(37, 99, 235, 0.12), transparent 25%),
            linear-gradient(135deg, #020617 0%, #071426 50%, #020617 100%) !important;
        color: #F8FAFC !important;
    }

    .main {
        background: transparent !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1500px !important;
    }

    p {
        color: #CBD5E1 !important;
    }

    h1 {
        color: #FFFFFF !important;
        font-weight: 900 !important;
        letter-spacing: -1.5px !important;
    }

    h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }

    label {
        color: #CBD5E1 !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #030B17 0%, #071426 50%, #020617 100%) !important;
        border-right: 1px solid rgba(34, 211, 238, 0.15) !important;
    }

    section[data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }

    .sidebar-brand {
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.25), rgba(37, 99, 235, 0.22));
        border: 1px solid rgba(34, 211, 238, 0.25);
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.04);
    }

    .sidebar-brand-small {
        color: #67E8F9 !important;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .sidebar-brand-title {
        color: #FFFFFF !important;
        font-size: 19px;
        font-weight: 900;
        margin-top: 7px;
    }

    .sidebar-brand-subtitle {
        color: #94A3B8 !important;
        font-size: 11px;
        margin-top: 3px;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 34px 38px;
        margin-bottom: 28px;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.16), rgba(37, 99, 235, 0.13), rgba(15, 23, 42, 0.95));
        border: 1px solid rgba(34, 211, 238, 0.18);
        box-shadow: 0 20px 50px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.04);
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 999px;
        background: rgba(6, 182, 212, 0.12);
        border: 1px solid rgba(34, 211, 238, 0.25);
        color: #67E8F9 !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 13px;
    }

    .hero-title {
        color: #FFFFFF !important;
        font-size: 42px;
        line-height: 1.1;
        font-weight: 900;
        letter-spacing: -2px;
        margin: 0;
    }

    .hero-title span {
        color: #22D3EE !important;
    }

    .hero-description {
        color: #94A3B8 !important;
        font-size: 15px;
        line-height: 1.7;
        max-width: 850px;
        margin-top: 12px;
    }

    .login-top {
        text-align: center;
        padding: 22px;
        margin-bottom: 35px;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.35), rgba(15, 23, 42, 0.85));
        border: 1px solid rgba(52, 211, 153, 0.20);
    }

    .login-top-arabic {
        color: #6EE7B7 !important;
        font-size: 23px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .login-top-darood {
        color: #A7F3D0 !important;
        font-size: 14px;
        line-height: 1.7;
    }

    .login-title {
        text-align: center;
        font-size: 58px;
        font-weight: 900;
        color: #FFFFFF !important;
        letter-spacing: -3px;
        margin-bottom: 0;
    }

    .login-subtitle {
        text-align: center;
        color: #22D3EE !important;
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 25px;
    }

    .login-description {
        text-align: center;
        max-width: 800px;
        margin: auto;
        color: #94A3B8 !important;
        line-height: 1.8;
        font-size: 15px;
    }

    .security-box {
        background: linear-gradient(145deg, rgba(15, 31, 52, 0.98), rgba(5, 18, 32, 0.98));
        border: 1px solid rgba(34, 211, 238, 0.20);
        border-radius: 20px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    }

    .security-title {
        color: #FFFFFF !important;
        text-align: center;
        font-weight: 800;
        font-size: 18px;
        margin-bottom: 15px;
    }

    .access-guide {
        background: rgba(8, 47, 73, 0.55);
        border-left: 4px solid #22D3EE;
        padding: 14px;
        border-radius: 10px;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .access-guide p {
        color: #BAE6FD !important;
        font-size: 13px;
        margin: 0;
        line-height: 1.6;
    }

    input,
    textarea {
        background-color: #0B1B2E !important;
        color: #FFFFFF !important;
        border: 1px solid #24435E !important;
        border-radius: 11px !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #64748B !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #0B1B2E !important;
        color: #FFFFFF !important;
        border: 1px solid #24435E !important;
        border-radius: 11px !important;
    }

    div[data-baseweb="select"] span {
        color: #FFFFFF !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #0891B2 0%, #2563EB 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(103, 232, 249, 0.25) !important;
        border-radius: 11px !important;
        font-weight: 800 !important;
        padding: 11px 20px !important;
        min-height: 45px !important;
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.15) !important;
        transition: all 0.25s ease !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        border-color: #67E8F9 !important;
        box-shadow: 0 12px 30px rgba(14, 165, 233, 0.28) !important;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(14, 31, 51, 0.98), rgba(6, 19, 33, 0.98)) !important;
        border: 1px solid rgba(34, 211, 238, 0.16) !important;
        border-radius: 17px !important;
        padding: 20px 23px !important;
        min-height: 115px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.22) !important;
    }

    div[data-testid="stMetric"]:hover {
        border-color: rgba(34, 211, 238, 0.40) !important;
        transform: translateY(-2px);
        transition: 0.2s ease;
    }

    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 31px !important;
        font-weight: 900 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 11px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    button[data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        border-radius: 9px 9px 0 0 !important;
        padding: 11px 15px !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #67E8F9 !important;
        background: rgba(6, 182, 212, 0.06) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #67E8F9 !important;
        background: rgba(6, 182, 212, 0.08) !important;
        border-bottom: 3px solid #22D3EE !important;
    }

    [data-testid="stFileUploader"] {
        background: rgba(7, 24, 40, 0.75) !important;
        border: 1px dashed rgba(34, 211, 238, 0.35) !important;
        border-radius: 16px !important;
        padding: 10px !important;
    }

    [data-testid="stFileUploader"] section {
        background: transparent !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid rgba(34, 211, 238, 0.15) !important;
        border-radius: 15px !important;
        overflow: hidden !important;
    }

    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    hr {
        border-color: rgba(148, 163, 184, 0.10) !important;
    }

    .footer {
        text-align: center;
        margin-top: 45px;
        padding: 20px;
        color: #64748B !important;
        font-size: 12px;
        border-top: 1px solid rgba(148,163,184,0.08);
    }

    .footer strong {
        color: #22D3EE !important;
    }

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #020617;
    }

    ::-webkit-scrollbar-thumb {
        background: #164E63;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #0891B2;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SESSION STATE
# ============================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ============================================================
# 🔐 LOGIN / FRONT PAGE
# ============================================================
if not st.session_state.logged_in:

    st.markdown(
        """
        <div class="login-top">
            <div class="login-top-arabic">
                بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
            </div>
            <div class="login-top-darood">
                أَللّٰهُمَّ صَلِّ عَلٰى مُحَمَّدٍ وَّعَلٰى آلِ مُحَمَّدٍ
                كَمَا صَلَّيْتَ عَلٰى إِبْرَاهِيْمَ وَعَلٰى آلِ إِبْرَاهِيْمَ
                إِنَّكَ حَمِيْدٌ مَّجِيْدٌ
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div>
            <div class="login-title">Universal.DA</div>
            <div class="login-subtitle">AI Agent By HI</div>
            <div class="login-description">
                A next-generation intelligent data analytics workspace
                designed to transform raw data into meaningful insights,
                visualizations, predictions, and professional reports.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.15, 1])

    with col2:

        st.markdown(
            """
            <div class="security-box">
                <div class="security-title">🔐 Secure Workspace Access</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        entered_password = st.text_input(
            "Gateway Password",
            type="password",
            placeholder="Enter security token..."
        )

        st.markdown(
            """
            <div class="access-guide">
                <p>
                    🔑 <b>Access Guide:</b>
                    Enter the authorized security token and
                    activate the analytics workspace.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("🚀 Unlock Gateway & Enter Workspace", use_container_width=True):

            if entered_password == "56-DA Agent":
                st.session_state.logged_in = True
                st.success("Access Authorized. Loading analytics workspace...")
                st.rerun()
            else:
                st.error("Access Refused. Invalid security token.")

    st.markdown(
        """
        <div class="footer">
            <strong>Universal.DA</strong>
            &nbsp; | &nbsp;
            AI-Powered Data Analytics Platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# 📊 MAIN WORKSPACE
# ============================================================

config.setup_page()
config.render_header()
config.init_session_state()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-small">✦ Intelligence Engine Active</div>
            <div class="sidebar-brand-title">Universal.DA</div>
            <div class="sidebar-brand-subtitle">AI Data Analytics Workspace</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("⚙️ Data Source")

    data_source = st.radio(
        "Choose your data source:",
        ["📁 Upload File", "🗄️ Database Connection", "🌐 API / Web URL"]
    )

    st.markdown("---")

    st.header("🤖 AI Configuration")

    env_api_key = os.getenv("GEMINI_API_KEY")

    secrets_api_key = None

    try:
        if "GEMINI_API_KEY" in st.secrets:
            secrets_api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    final_key = env_api_key or secrets_api_key

    if final_key:
        st.success("✅ API Key loaded automatically!")
        api_key = final_key
    else:
        st.warning("⚠️ No API key found in system environment")
        api_key = st.text_input("Enter Gemini API Key manually", type="password")

    ai_model = st.selectbox("AI Model", ["gemini-3.6-flash"])

    st.markdown("---")

    if st.button("🔒 Lock Workspace & Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("Universal.DA • AI Analytics • v1.0")


# ============================================================
# 🌐 WORKSPACE HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">✦ AI POWERED ANALYTICS ENGINE</div>
        <div class="hero-title">Universal.<span>DA</span></div>
        <div class="hero-description">
            Transform your data into actionable intelligence through
            automated analysis, visualization, AI-powered insights,
            forecasting, and professional reporting.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 📥 DATA LOADING
# ============================================================

if data_source == "📁 Upload File":
    data_loading.render_file_upload()
elif data_source == "🗄️ Database Connection":
    data_loading.render_database_connection()
elif data_source == "🌐 API / Web URL":
    data_loading.render_api_fetch()


# ============================================================
# MAIN CONTENT
# ============================================================

df = st.session_state.df


if df is not None:

    st.markdown(
        """
        <div style="
            color:#67E8F9;
            font-size:13px;
            font-weight:800;
            letter-spacing:1px;
            margin-bottom:12px;
            text-transform:uppercase;
        ">
            ✦ Dataset Intelligence Overview
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Rows", f"{df.shape[0]:,}")

    with col2:
        st.metric("Total Columns", f"{df.shape[1]:,}")

    with col3:
        st.metric("Missing Values", f"{df.isnull().sum().sum():,}")

    with col4:
        st.metric("Duplicate Rows", f"{df.duplicated().sum():,}")

    st.markdown("<br>", unsafe_allow_html=True)

    (
        tab1, tab_p, tab2, tab3, tab4, tab5, tab6, tab7, tab8
    ) = st.tabs(
        [
            "🔍 Data Preview",
            "🧬 Data Profile",
            "🧹 Data Cleaning",
            "📈 Statistics",
            "🔗 Correlations",
            "📊 Visualizations",
            "🤖 AI Insights",
            "🔮 Forecasting",
            "📑 Final Report"
        ]
    )

    with tab1:
        tab_preview.render(df)

    with tab_p:
        tab_profile.render(df)

    with tab2:
        tab_cleaning.render(df)

    with tab3:
        tab_stats.render(df)

    with tab4:
        tab_correlations.render(df)

    with tab5:
        tab_visualizations.render(df)

    with tab6:
        tab_ai_insights.render(df, api_key, ai_model)

    with tab7:
        tab_forecasting.render(df)

    with tab8:
        tab_final_report.render(df)

else:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:70px 30px;
            margin-top:30px;
            background: linear-gradient(145deg, rgba(14,31,51,0.75), rgba(5,18,32,0.75));
            border:1px dashed rgba(34,211,238,0.25);
            border-radius:22px;
        ">
            <div style="font-size:48px; margin-bottom:15px;">📊</div>
            <h3 style="color:#FFFFFF !important; margin-bottom:8px;">No Dataset Loaded</h3>
            <p style="color:#94A3B8 !important; font-size:14px;">
                Upload a file, connect to a database,
                or fetch data from an API to begin your analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <strong>Universal.DA</strong>
        &nbsp; • &nbsp;
        AI-Powered Data Analytics
        &nbsp; • &nbsp;
        Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)