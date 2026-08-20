import pandas as pd


# ============================================================
# DATA PROFILING FUNCTION
# PHASE 1 - STEP 1
# ============================================================

def generate_data_profile(dataframe):
    """
    Har column ka deep profile nikalta hai:
    - Null Percentage
    - Unique Values Count
    - Suspected Data Category
    """

    profile_rows = []
    total_rows = len(dataframe)

    for col in dataframe.columns:

        col_data = dataframe[col]

        null_pct = round(
            (col_data.isnull().sum() / total_rows) * 100, 2
        ) if total_rows > 0 else 0

        unique_count = col_data.nunique()
        col_name_lower = col.lower()
        dtype = str(col_data.dtype)

        # ---- Suspected Category Logic ----

        if "datetime" in dtype:
            category = "📅 Date"

        elif any(keyword in col_name_lower for keyword in ["id", "code", "number", "no"]) and unique_count == total_rows:
            category = "🔑 Identifier"

        elif any(keyword in col_name_lower for keyword in ["price", "amount", "cost", "sales", "profit", "revenue", "salary"]):
            category = "💰 Monetary"

        elif any(keyword in col_name_lower for keyword in ["email"]):
            category = "📧 Email"

        elif any(keyword in col_name_lower for keyword in ["phone", "contact"]):
            category = "📞 Phone"

        elif any(keyword in col_name_lower for keyword in ["name"]):
            category = "👤 Name"

        elif dtype in ["int64", "float64"] and unique_count <= 10:
            category = "🔢 Numeric Flag/Rating"

        elif dtype in ["int64", "float64"]:
            category = "📊 Numeric Measure"

        elif dtype == "object" and unique_count <= max(20, total_rows * 0.05):
            category = "🏷️ Category/Label"

        elif dtype == "object" and unique_count == total_rows:
            category = "🔑 Identifier"

        else:
            category = "📝 Free Text"

        profile_rows.append({
            "Column": col,
            "Data Type": dtype,
            "Null %": null_pct,
            "Unique Values": unique_count,
            "Suspected Category": category
        })

    return pd.DataFrame(profile_rows)


# ============================================================
# OUTLIER DETECTION FUNCTIONS
# PHASE 1 - STEP 2
# ============================================================

def detect_outliers_iqr(dataframe, column):
    """
    IQR method se ek column ke outliers dhoondta hai.
    Returns: outlier rows ka DataFrame, lower bound, upper bound
    """

    Q1 = dataframe[column].quantile(0.25)
    Q3 = dataframe[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - (1.5 * IQR)
    upper_bound = Q3 + (1.5 * IQR)

    outlier_mask = (dataframe[column] < lower_bound) | (dataframe[column] > upper_bound)
    outlier_rows = dataframe[outlier_mask]

    return outlier_rows, lower_bound, upper_bound


def get_all_outlier_summary(dataframe):
    """
    Har numeric column ke outliers ka summary nikalta hai.
    """

    numeric_cols = dataframe.select_dtypes(include=["number"]).columns
    summary_rows = []

    for col in numeric_cols:
        outliers, lower, upper = detect_outliers_iqr(dataframe, col)
        summary_rows.append({
            "Column": col,
            "Outlier Count": len(outliers),
            "Lower Bound": round(lower, 2),
            "Upper Bound": round(upper, 2),
            "Min Value": round(dataframe[col].min(), 2),
            "Max Value": round(dataframe[col].max(), 2)
        })

    return pd.DataFrame(summary_rows)