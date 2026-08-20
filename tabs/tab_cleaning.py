import streamlit as st
import pandas as pd
from utils.data_profiling import detect_outliers_iqr, get_all_outlier_summary


def render(df):
    """Data Cleaning tab render karta hai (Duplicates, Missing, Dates, Outliers)."""

    st.subheader("Data Cleaning Tools")

    col1, col2, col3 = st.columns(3)

    # --------------------------------------------------
    # DUPLICATES
    # --------------------------------------------------

    with col1:
        st.markdown("**🔁 Duplicate Rows**")
        st.write(f"Found: **{df.duplicated().sum()}** duplicates")

        if st.button("🗑️ Remove Duplicates", use_container_width=True):
            before = len(df)
            st.session_state.df = df.drop_duplicates()
            after = len(st.session_state.df)
            st.success(f"Removed {before - after} duplicate rows!")
            st.rerun()

    # --------------------------------------------------
    # MISSING VALUES
    # --------------------------------------------------

    with col2:
        st.markdown("**🕳️ Missing Values**")
        st.write(f"Found: **{df.isnull().sum().sum()}** missing values")

        if st.button("🧩 Fill Missing (Numeric = Mean, Text = Mode)", use_container_width=True):
            new_df = df.copy()

            for col in new_df.columns:
                if pd.api.types.is_numeric_dtype(new_df[col]):
                    new_df[col] = new_df[col].fillna(new_df[col].mean())
                else:
                    mode_values = new_df[col].mode()
                    if not mode_values.empty:
                        new_df[col] = new_df[col].fillna(mode_values.iloc[0])

            st.session_state.df = new_df
            st.success("Missing values filled!")
            st.rerun()

    # --------------------------------------------------
    # DATE DETECTION
    # --------------------------------------------------

    with col3:
        st.markdown("**📅 Auto-Detect Dates**")
        st.write("Convert text columns to dates")

        if st.button("🔄 Auto-Convert Date Columns", use_container_width=True):
            new_df = df.copy()
            converted_cols = []

            for col in new_df.select_dtypes(include=["object"]).columns:
                try:
                    converted = pd.to_datetime(new_df[col], errors="coerce")
                    if converted.notna().sum() / len(new_df) > 0.8:
                        new_df[col] = converted
                        converted_cols.append(col)
                except Exception:
                    pass

            st.session_state.df = new_df

            if converted_cols:
                st.success("Converted columns: " + ", ".join(converted_cols))
            else:
                st.info("No date-like columns detected.")

            st.rerun()

    st.divider()

    st.subheader("Cleaned Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.divider()

    # ====================================================
    # OUTLIER DETECTION SECTION
    # PHASE 1 - STEP 2
    # ====================================================

    st.subheader("🎯 Automated Outlier Detection")
    st.caption("IQR method se aisi values dhoondi jati hain jo data ko distort kar sakti hain")

    numeric_cols_for_outliers = df.select_dtypes(include=["number"]).columns.tolist()

    if not numeric_cols_for_outliers:
        st.info("No numeric columns found for outlier detection.")
    else:
        outlier_summary = get_all_outlier_summary(df)
        st.dataframe(outlier_summary, use_container_width=True)

        total_outliers = outlier_summary["Outlier Count"].sum()

        if total_outliers == 0:
            st.success("✅ No significant outliers detected in your data.")
        else:
            st.warning(f"⚠️ Found **{total_outliers}** potential outlier value(s) across your numeric columns.")

            selected_outlier_col = st.selectbox(
                "Select a column to inspect its outliers",
                outlier_summary[outlier_summary["Outlier Count"] > 0]["Column"].tolist()
            )

            if selected_outlier_col:
                outlier_rows, lower, upper = detect_outliers_iqr(df, selected_outlier_col)

                st.write(f"**Normal range:** {lower:.2f} to {upper:.2f}")
                st.dataframe(outlier_rows, use_container_width=True)

                col_a, col_b = st.columns(2)

                with col_a:
                    if st.button(f"🗑️ Remove Outliers from '{selected_outlier_col}'", use_container_width=True):
                        before = len(df)
                        outlier_indices = outlier_rows.index
                        st.session_state.df = df.drop(index=outlier_indices).reset_index(drop=True)
                        after = len(st.session_state.df)
                        st.success(f"Removed {before - after} outlier row(s) from '{selected_outlier_col}'!")
                        st.rerun()

                with col_b:
                    st.info("💡 Only remove outliers if you're sure they are data entry errors, not real extreme values.")