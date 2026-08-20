import streamlit as st


def setup_page():
    """Page configuration aur custom CSS setup karta hai."""

    st.set_page_config(
        page_title="DA Agent",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
    <style>

    .block-container {
        padding-top: 3rem !important;
    }

    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        padding-bottom: 0px;
        margin-bottom: 0px;
        margin-top: 0px;
    }

    .sub-header {
        font-size: 1rem;
        color: #6B7280;
        margin-top: 0px;
        margin-bottom: 2rem;
    }

    .stFileUploader {
        border: 2px dashed #1E3A8A;
        border-radius: 10px;
        padding: 20px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #1E3A8A;
    }

    .ai-report-box {
        background-color: #F3F4F6;
        border-left: 4px solid #1E3A8A;
        padding: 20px;
        border-radius: 8px;
    }

    .report-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 20px;
        margin-top: 10px;
    }

    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Main title aur subtitle dikhata hai."""

    st.markdown(
        '<p class="main-header">📊 DA Agent</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="sub-header">Your AI-powered Data Analysis Assistant</p>',
        unsafe_allow_html=True
    )

    st.divider()


def init_session_state():
    """Sab session state variables ko initialize karta hai."""

    defaults = {
        "df": None,
        "ai_report": None,
        "forecast_result": None,
        "forecast_fig_html": None,
        "forecast_model_slope": None,
        "forecast_date_column": None,
        "forecast_sales_column": None,
        "html_report": None,
        "pdf_report": None,
        "data_profile": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_generated_reports():
    """Jab nayi data load ho, purane reports clear kar deta hai."""

    st.session_state.ai_report = None
    st.session_state.forecast_result = None
    st.session_state.forecast_fig_html = None
    st.session_state.html_report = None
    st.session_state.pdf_report = None
    st.session_state.data_profile = None