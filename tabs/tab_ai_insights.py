import streamlit as st
from google import genai as google_genai


def render(df, api_key, ai_model):
    """AI Insights tab render karta hai — Gemini se business analysis."""

    st.subheader("🤖 AI-Powered Business Insights")

    st.write(
        "Get a deep business analysis of your data — "
        "trends, anomalies, and actionable recommendations."
    )

    if not api_key:
        st.warning("⚠️ Please provide a Gemini API Key to use this feature.")
        return

    generate_btn = st.button("✨ Generate AI Report", type="primary", use_container_width=True)

    if generate_btn:
        numeric_df = df.select_dtypes(include=["number"])

        if numeric_df.empty:
            st.error("No numeric columns found — cannot generate meaningful statistical insights.")
        else:
            try:
                with st.spinner("🧠 AI is analyzing your data... this may take a few seconds"):

                    stats_text = numeric_df.describe().to_string()

                    corr_text = (
                        numeric_df.corr(numeric_only=True).to_string()
                        if numeric_df.shape[1] >= 2
                        else "Not enough numeric columns for correlation."
                    )

                    prompt = f"""
You are a Master Data Analyst.

Analyze this dataset summary:

Columns:
{list(df.columns)}

Total Rows:
{df.shape[0]}

Total Columns:
{df.shape[1]}

Missing Values:
{df.isnull().sum().sum()}

Duplicate Rows:
{df.duplicated().sum()}

Basic Stats:
{stats_text}

Correlations:
{corr_text}

Please provide a deep business analysis with the following structure using markdown headings:

## 📊 Top Trends & Patterns

List 3 key trends or patterns visible in this data.

## ⚠️ Data Anomalies & Issues

Point out any outliers, unusual distributions, or data quality issues.

## 💡 Actionable Recommendations

Give clear, practical business advice based on these statistics.

## 🎯 Business Conclusion

Give a concise overall conclusion about the dataset.
"""

                    client = google_genai.Client(api_key=api_key)

                    response = client.models.generate_content(
                        model=ai_model,
                        contents=prompt
                    )

                    ai_output = response.text
                    st.session_state.ai_report = ai_output

                    # Old generated reports are no longer current
                    st.session_state.html_report = None
                    st.session_state.pdf_report = None

            except Exception as e:
                st.error(f"❌ Failed to generate AI report: {e}")

    if st.session_state.ai_report:
        st.divider()

        st.markdown('<div class="ai-report-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.ai_report)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            "📥 Download AI Report",
            st.session_state.ai_report,
            file_name="ai_business_report.md",
            mime="text/markdown"
        )