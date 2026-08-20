import streamlit as st


def render(df):
    """Correlations tab render karta hai."""

    st.subheader("🔗 Correlation Matrix")

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] >= 2:
        corr_matrix = numeric_df.corr(numeric_only=True)

        st.dataframe(
            corr_matrix.style.background_gradient(cmap="Blues").format("{:.2f}"),
            use_container_width=True
        )

        st.session_state.correlation_metadata = corr_matrix.to_dict()

    else:
        st.info("Need at least 2 numeric columns to calculate correlations.")