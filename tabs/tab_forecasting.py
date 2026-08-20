import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression


def render(df):
    """30-Day Sales Forecasting tab render karta hai."""

    st.subheader("🔮 30-Day Sales Forecast")

    st.write(
        "Use Scikit-Learn Linear Regression "
        "to predict the next 30 days of sales "
        "based on historical data."
    )

    # ----------------------------------------------------
    # FIND DATE COLUMNS
    # ----------------------------------------------------

    date_column_candidates = [
        col for col in df.columns
        if col.lower().strip() in [
            "date", "sales_date", "order_date",
            "order_purchase_date", "purchase_date",
            "datetime", "order purchase date"
        ]
    ]

    if not date_column_candidates:
        date_column_candidates = [
            col for col in df.columns
            if any(word in col.lower() for word in ["date", "datetime", "time"])
        ]

    # ----------------------------------------------------
    # FIND SALES COLUMNS
    # ----------------------------------------------------

    sales_column_candidates = [
        col for col in df.columns
        if col.lower().strip() in [
            "sales", "sale", "revenue", "total_sales", "total sales"
        ]
    ]

    if not sales_column_candidates:
        sales_column_candidates = [
            col for col in df.columns
            if any(word in col.lower() for word in ["sales", "revenue"])
        ]

    # ----------------------------------------------------
    # VALIDATION
    # ----------------------------------------------------

    if not date_column_candidates:
        st.warning("⚠️ No Date column found. Please make sure your dataset contains a Date column.")
        return

    if not sales_column_candidates:
        st.warning("⚠️ No Sales/Revenue column found. Please make sure your dataset contains a Sales or Revenue column.")
        return

    date_column = st.selectbox("📅 Select Date Column", date_column_candidates, key="forecast_date_selector")
    sales_column = st.selectbox("💰 Select Sales Column", sales_column_candidates, key="forecast_sales_selector")

    if st.button("🔮 Generate 30-Day Forecast", type="primary", use_container_width=True):

        try:
            with st.spinner("🧠 Training Linear Regression model..."):

                forecast_df = df[[date_column, sales_column]].copy()

                forecast_df[date_column] = pd.to_datetime(forecast_df[date_column], errors="coerce")
                forecast_df[sales_column] = pd.to_numeric(forecast_df[sales_column], errors="coerce")

                forecast_df = forecast_df.dropna(subset=[date_column, sales_column])

                if forecast_df.empty:
                    st.error("❌ No valid Date and Sales data available.")
                    return

                daily_sales = (
                    forecast_df.groupby(date_column)[sales_column]
                    .sum()
                    .reset_index()
                    .sort_values(date_column)
                )

                if len(daily_sales) < 2:
                    st.error("❌ At least 2 different dates are required.")
                    return

                first_date = daily_sales[date_column].min()
                daily_sales["day_number"] = (daily_sales[date_column] - first_date).dt.days

                X = daily_sales[["day_number"]]
                y = daily_sales[sales_column]

                model = LinearRegression()
                model.fit(X, y)

                last_date = daily_sales[date_column].max()

                future_dates = pd.date_range(
                    start=(last_date + pd.Timedelta(days=1)),
                    periods=30,
                    freq="D"
                )

                future_day_numbers = (future_dates - first_date).days
                future_X = pd.DataFrame({"day_number": future_day_numbers})

                predictions = model.predict(future_X)
                predictions = pd.Series(predictions).clip(lower=0).values

                forecast_result = pd.DataFrame({
                    "Date": future_dates,
                    "Predicted Sales": predictions
                })

                # ---- SAVE TO SESSION STATE ----

                st.session_state.forecast_result = forecast_result.copy()
                st.session_state.forecast_model_slope = float(model.coef_[0])
                st.session_state.forecast_date_column = date_column
                st.session_state.forecast_sales_column = sales_column

                # ---- HISTORICAL + FORECAST GRAPH ----

                historical_plot = daily_sales[[date_column, sales_column]].copy()
                historical_plot.columns = ["Date", "Sales"]
                historical_plot["Type"] = "Historical"

                forecast_plot = forecast_result[["Date", "Predicted Sales"]].copy()
                forecast_plot.columns = ["Date", "Sales"]
                forecast_plot["Type"] = "Forecast"

                combined_plot = pd.concat([historical_plot, forecast_plot], ignore_index=True)

                fig_forecast = px.line(
                    combined_plot, x="Date", y="Sales", color="Type",
                    title="Historical Sales and 30-Day Forecast",
                    markers=True
                )

                fig_forecast.update_layout(
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    font=dict(color="#111827"),
                    title_font=dict(size=18, color="#1E3A8A"),
                    margin=dict(t=60, b=40, l=40, r=40)
                )

                st.session_state.forecast_fig_html = fig_forecast.to_html(
                    full_html=False, include_plotlyjs=True
                )

                st.success("✅ 30-day forecast generated successfully!")

                # ---- METRICS ----

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Historical Days", f"{len(daily_sales):,}")

                with col2:
                    st.metric("Forecast Days", "30")

                with col3:
                    st.metric("Predicted Total Sales", f"{predictions.sum():,.2f}")

                # ---- TABLE ----

                st.subheader("📋 30-Day Forecast")

                display_forecast = forecast_result.copy()
                display_forecast["Date"] = display_forecast["Date"].dt.strftime("%Y-%m-%d")
                display_forecast["Predicted Sales"] = display_forecast["Predicted Sales"].round(2)

                st.dataframe(display_forecast, use_container_width=True)

                # ---- GRAPH ----

                st.subheader("📈 Historical Sales + 30-Day Forecast")
                st.plotly_chart(fig_forecast, use_container_width=True)

                # ---- MODEL INFO ----

                st.subheader("🤖 Forecast Model Information")
                st.write("Model: **Linear Regression**")
                st.write(f"Training Data Points: **{len(daily_sales):,} days**")
                st.write("Forecast Horizon: **30 days**")
                st.write(f"Trend/Slope: **{model.coef_[0]:,.4f}**")

                if model.coef_[0] > 0:
                    st.success("📈 The model detects an increasing historical trend.")
                elif model.coef_[0] < 0:
                    st.warning("📉 The model detects a decreasing historical trend.")
                else:
                    st.info("➡️ The model detects a relatively flat trend.")

        except Exception as e:
            st.error(f"❌ Forecasting failed: {e}")
            st.caption("Please make sure the selected Date and Sales columns contain valid values.")

    # ----------------------------------------------------
    # DISPLAY EXISTING FORECAST AFTER RERUN
    # ----------------------------------------------------

    if st.session_state.forecast_result is not None:
        st.divider()
        st.info("A forecast is currently available and will be included in the final report.")
