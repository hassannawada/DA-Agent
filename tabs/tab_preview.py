import streamlit as st
import pandas as pd


def render(df):
    """Data Preview tab render karta hai."""

    st.subheader("Data Preview")

    preview_rows = min(len(df), 5000)

    st.dataframe(
        df.head(preview_rows),
        use_container_width=True
    )

    st.caption(
        f"Showing {preview_rows:,} of {len(df):,} total rows"
    )

    st.subheader("Column Data Types")

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Non-Null Count": df.count().values,
        "Null Count": df.isnull().sum().values
    })

    st.dataframe(dtype_df, use_container_width=True)