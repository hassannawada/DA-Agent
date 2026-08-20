import streamlit as st
from utils.report_generator import generate_html_report, generate_pdf_report


def render(df):
    """Final Report tab render karta hai — HTML + PDF generation."""

    st.subheader("📑 Final Report Generator")

    st.write(
        "Generate a complete downloadable report "
        "containing dataset information, statistics, "
        "correlations, AI insights, and 30-day forecasting."
    )

    # ---- PREVIEW METRICS ----

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rows", f"{len(df):,}")

    with col2:
        st.metric("Columns", f"{len(df.columns):,}")

    with col3:
        st.metric("Missing Values", f"{df.isnull().sum().sum():,}")

    with col4:
        forecast_status = "Available" if st.session_state.forecast_result is not None else "Not Generated"
        st.metric("Forecast", forecast_status)

    st.divider()

    # ---- REPORT CONTENT STATUS ----

    st.subheader("📋 Report Contents")

    report_items = [
        ("Dataset Overview", True),
        ("Column Information", True),
        ("Statistical Analysis", True),
        ("Correlation Analysis", df.select_dtypes(include=["number"]).shape[1] >= 2),
        ("AI Business Insights", st.session_state.ai_report is not None),
        ("30-Day Sales Forecast", st.session_state.forecast_result is not None),
        ("Interactive Plotly Forecast Chart", st.session_state.forecast_fig_html is not None)
    ]

    for item, available in report_items:
        if available:
            st.success(f"✅ {item}")
        else:
            st.warning(f"⚠️ {item} not available")

    st.divider()

    # ---- GENERATE HTML REPORT ----

    if st.button("📑 Generate Complete HTML Report", type="primary", use_container_width=True):

        html_report = generate_html_report(
            df,
            st.session_state.ai_report,
            st.session_state.forecast_result,
            st.session_state.forecast_fig_html,
            st.session_state.forecast_model_slope
        )

        st.session_state.html_report = html_report

        st.success("✅ Complete HTML report generated successfully!")

    if st.session_state.html_report:

        st.download_button(
            label="📥 Download Complete HTML Report",
            data=st.session_state.html_report,
            file_name="DA_Agent_Final_Report.html",
            mime="text/html",
            use_container_width=True
        )

        st.info("💡 Open the downloaded HTML file in Chrome, Edge, Firefox, or another browser.")

    st.divider()

    # ---- PDF REPORT ----

    st.subheader("📄 PDF Report")
    st.write("Generate a printable PDF version of the final analysis report.")

    if st.button("📄 Generate PDF Report", use_container_width=True):

        try:
            pdf_bytes = generate_pdf_report(
                df,
                st.session_state.ai_report,
                st.session_state.forecast_result,
                st.session_state.forecast_model_slope
            )

            st.session_state.pdf_report = pdf_bytes

            st.success("✅ PDF report generated successfully!")

        except Exception as e:
            st.error(f"❌ PDF generation failed: {e}")

    if st.session_state.pdf_report:

        st.download_button(
            label="📥 Download Complete PDF Report",
            data=st.session_state.pdf_report,
            file_name="DA_Agent_Final_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
