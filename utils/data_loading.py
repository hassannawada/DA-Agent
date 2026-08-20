import streamlit as st
import pandas as pd
import requests
from sqlalchemy import create_engine
import config


def render_file_upload():
    """File upload option render karta hai aur data load karta hai."""

    st.subheader("📁 Upload Your Data")

    uploaded_file = st.file_uploader(
        "Drag and drop or browse for a CSV / Excel file",
        type=["csv", "xlsx"],
        help="Supported formats: CSV, XLSX"
    )

    if uploaded_file:

        with st.spinner("Loading your data..."):

            if uploaded_file.name.endswith(".csv"):
                new_df = pd.read_csv(uploaded_file)
            else:
                new_df = pd.read_excel(uploaded_file)

        st.session_state.df = new_df
        config.reset_generated_reports()

        st.success(f"✅ **{uploaded_file.name}** loaded successfully!")


def render_database_connection():
    """Database connection form render karta hai aur data fetch karta hai."""

    st.subheader("🗄️ Connect to Database")

    with st.form("db_connection_form"):

        col1, col2 = st.columns(2)

        with col1:
            db_host = st.text_input("Host", placeholder="localhost")
            db_user = st.text_input("Username", placeholder="root")
            db_name = st.text_input("Database Name", placeholder="my_database")

        with col2:
            db_port = st.text_input("Port", placeholder="3306")
            db_password = st.text_input("Password", type="password")
            db_table = st.text_input("Table Name", placeholder="sales_data")

        connect_btn = st.form_submit_button("🔌 Connect & Fetch Data")

    if connect_btn:

        try:

            with st.spinner("Connecting to database..."):

                connection_string = (
                    f"mysql+mysqlconnector://"
                    f"{db_user}:{db_password}@"
                    f"{db_host}:{db_port}/{db_name}"
                )

                engine = create_engine(connection_string)
                query = f"SELECT * FROM {db_table}"
                new_df = pd.read_sql(query, engine)

            st.session_state.df = new_df
            config.reset_generated_reports()

            st.success(f"✅ Connected! Data fetched from **{db_table}** table")

        except Exception as e:
            st.error(f"❌ Connection failed: {e}")


def render_api_fetch():
    """API/Web URL se data fetch karta hai."""

    st.subheader("🌐 Fetch Data from API")

    api_url = st.text_input("Enter API URL", placeholder="https://api.example.com/data")
    fetch_btn = st.button("📥 Fetch Data")

    if fetch_btn and api_url:

        try:

            with st.spinner("Fetching data from API..."):

                response = requests.get(api_url, timeout=15)
                response.raise_for_status()
                json_data = response.json()

                if isinstance(json_data, list):
                    new_df = pd.DataFrame(json_data)

                elif isinstance(json_data, dict):
                    list_key = None

                    for key, value in json_data.items():
                        if isinstance(value, list):
                            list_key = key
                            break

                    if list_key:
                        new_df = pd.DataFrame(json_data[list_key])
                    else:
                        new_df = pd.DataFrame([json_data])

                else:
                    raise ValueError("Unsupported API response format.")

            st.session_state.df = new_df
            config.reset_generated_reports()

            st.success("✅ Data fetched successfully from API!")

        except Exception as e:
            st.error(f"❌ Failed to fetch data: {e}")