import streamlit as st
from utils.data_profiling import generate_data_profile


def render(df):
    """Data Profile & Validation tab render karta hai."""

    st.subheader("🧬 Data Profile & Validation")

    st.caption(
        "Master Analyst ki pehli nazar — "
        "har column ki quality aur suspected category"
    )

    profile_df = generate_data_profile(df)
    st.session_state.data_profile = profile_df

    pcol1, pcol2, pcol3 = st.columns(3)

    with pcol1:
        high_null_cols = (profile_df["Null %"] > 30).sum()
        st.metric("⚠️ Columns with >30% Nulls", high_null_cols)

    with pcol2:
        id_cols = profile_df["Suspected Category"].str.contains("Identifier").sum()
        st.metric("🔑 Identifier Columns", id_cols)

    with pcol3:
        numeric_cols_count = profile_df["Suspected Category"].str.contains("Monetary|Numeric").sum()
        st.metric("📊 Numeric/Monetary Columns", numeric_cols_count)

    st.divider()

    st.dataframe(
        profile_df.style.background_gradient(
            subset=["Null %"],
            cmap="Reds"
        ),
        use_container_width=True
    )

    risky_cols = profile_df[profile_df["Null %"] > 30]

    if not risky_cols.empty:
        st.warning(
            f"⚠️ **{len(risky_cols)} column(s)** have more than "
            f"30% missing data: "
            f"{', '.join(risky_cols['Column'].tolist())}. "
            f"Consider cleaning these in the Data Cleaning tab."
        )