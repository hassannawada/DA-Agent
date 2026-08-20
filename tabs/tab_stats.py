import streamlit as st


def render(df):
    """Statistics tab render karta hai."""

    st.subheader("📈 Core Statistical Summary")

    numeric_df = df.select_dtypes(include=["number"])

    if not numeric_df.empty:
        stats_summary = numeric_df.describe().T
        stats_summary["missing"] = df[numeric_df.columns].isnull().sum()

        st.dataframe(
            stats_summary.style.format("{:.2f}"),
            use_container_width=True
        )

        st.session_state.stats_metadata = stats_summary.to_dict()

    else:
        st.info("No numeric columns found for statistical analysis.")