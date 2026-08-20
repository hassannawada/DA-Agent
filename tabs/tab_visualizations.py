import streamlit as st
import plotly.express as px


def render(df):
    """Visualizations tab render karta hai — Dynamic Chart Builder."""

    st.subheader("📊 Dynamic Chart Builder")

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    text_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    date_cols = df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns.tolist()
    all_cols = df.columns.tolist()

    # ---- Auto-Suggest Chart Type ----

    if date_cols and numeric_cols:
        suggested_chart = "Line Chart"
    elif text_cols and numeric_cols:
        suggested_chart = "Bar Chart"
    elif len(numeric_cols) >= 2:
        suggested_chart = "Scatter Plot"
    else:
        suggested_chart = "Bar Chart"

    st.info(f"💡 Suggested chart type based on your data: **{suggested_chart}**")

    col1, col2, col3 = st.columns(3)

    with col1:
        chart_options = ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram", "Box Plot"]
        chart_type = st.selectbox(
            "Select Chart Type",
            chart_options,
            index=chart_options.index(suggested_chart)
        )

    with col2:
        x_axis = st.selectbox("X-Axis", all_cols)

    with col3:
        y_axis_options = ["None"] + numeric_cols
        y_axis = st.selectbox("Y-Axis", y_axis_options)

    color_col = st.selectbox("Color By (optional)", ["None"] + text_cols)

    try:
        color_arg = None if color_col == "None" else color_col
        y_arg = None if y_axis == "None" else y_axis

        if chart_type == "Bar Chart":
            fig = px.bar(
                df, x=x_axis, y=y_arg, color=color_arg,
                title=f"{x_axis} vs {y_axis}",
                color_discrete_sequence=px.colors.qualitative.Bold
            )

        elif chart_type == "Line Chart":
            fig = px.line(
                df, x=x_axis, y=y_arg, color=color_arg,
                title=f"{x_axis} vs {y_axis}",
                color_discrete_sequence=px.colors.qualitative.Bold
            )

        elif chart_type == "Scatter Plot":
            fig = px.scatter(
                df, x=x_axis, y=y_arg, color=color_arg,
                title=f"{x_axis} vs {y_axis}",
                color_discrete_sequence=px.colors.qualitative.Bold
            )

        elif chart_type == "Pie Chart":
            if y_axis == "None":
                fig = px.pie(df, names=x_axis, title=f"Distribution of {x_axis}")
            else:
                fig = px.pie(df, names=x_axis, values=y_axis, title=f"Distribution of {x_axis}")

        elif chart_type == "Histogram":
            fig = px.histogram(
                df, x=x_axis, color=color_arg,
                title=f"Distribution of {x_axis}",
                color_discrete_sequence=px.colors.qualitative.Bold
            )

        elif chart_type == "Box Plot":
            fig = px.box(
                df, x=x_axis, y=y_arg, color=color_arg,
                title=f"{x_axis} vs {y_axis}",
                color_discrete_sequence=px.colors.qualitative.Bold
            )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#111827"),
            title_font=dict(size=18, color="#1E3A8A"),
            margin=dict(t=60, b=40, l=40, r=40)
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Could not generate chart: {e}")
        st.caption("Try selecting different columns for X and Y axis.")