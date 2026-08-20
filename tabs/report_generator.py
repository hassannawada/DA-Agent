import pandas as pd
from html import escape
from datetime import datetime
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.units import inch


def convert_ai_to_html(text):
    """AI ke markdown report ko HTML mein convert karta hai."""

    if not text:
        return "<p>No AI report generated.</p>"

    lines = text.splitlines()
    html_parts = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            html_parts.append("<br>")
        elif stripped.startswith("### "):
            html_parts.append(f"<h3>{escape(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            html_parts.append(f"<h2>{escape(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            html_parts.append(f"<h1>{escape(stripped[2:])}</h1>")
        elif stripped.startswith("- "):
            html_parts.append(f"<li>{escape(stripped[2:])}</li>")
        elif stripped.startswith("* "):
            html_parts.append(f"<li>{escape(stripped[2:])}</li>")
        else:
            html_parts.append(f"<p>{escape(stripped)}</p>")

    return "\n".join(html_parts)


def generate_html_report(df, ai_report, forecast_result, forecast_fig_html, forecast_model_slope):
    """Complete HTML report banata hai aur string return karta hai."""

    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_rows = df.shape[0]
    total_columns = df.shape[1]
    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    # ---- COLUMN INFO TABLE ----

    column_rows = ""
    for column in df.columns:
        column_rows += f"""
        <tr>
            <td>{escape(str(column))}</td>
            <td>{escape(str(df[column].dtype))}</td>
            <td>{df[column].count():,}</td>
            <td>{df[column].isnull().sum():,}</td>
        </tr>
        """

    column_table = f"""
    <table class="data-table">
        <thead>
            <tr>
                <th>Column</th><th>Data Type</th><th>Non-Null</th><th>Missing</th>
            </tr>
        </thead>
        <tbody>{column_rows}</tbody>
    </table>
    """

    # ---- STATISTICS ----

    numeric_df = df.select_dtypes(include=["number"])

    if not numeric_df.empty:
        statistics_html = numeric_df.describe().T.round(2).to_html(classes="data-table", border=0)
    else:
        statistics_html = "<p>No numeric columns available.</p>"

    # ---- CORRELATIONS ----

    if numeric_df.shape[1] >= 2:
        correlation_html = numeric_df.corr(numeric_only=True).round(2).to_html(classes="data-table", border=0)
    else:
        correlation_html = "<p>Not enough numeric columns for correlation analysis.</p>"

    # ---- AI REPORT ----

    ai_html = convert_ai_to_html(ai_report)

    # ---- FORECAST ----

    if forecast_result is not None:

        forecast_report_df = forecast_result.copy()
        forecast_report_df["Date"] = forecast_report_df["Date"].dt.strftime("%Y-%m-%d")
        forecast_report_df["Predicted Sales"] = forecast_report_df["Predicted Sales"].round(2)

        forecast_html = forecast_report_df.to_html(classes="data-table", border=0, index=False)

        forecast_total = forecast_result["Predicted Sales"].sum()

        forecast_summary = f"""
        <div class="summary-box">
            <p><strong>Forecast Horizon:</strong> 30 days</p>
            <p><strong>Predicted Total Sales:</strong> {forecast_total:,.2f}</p>
            <p><strong>Trend/Slope:</strong> {forecast_model_slope:,.4f}</p>
        </div>
        """

        forecast_chart_html = forecast_fig_html if forecast_fig_html else "<p>Forecast chart is not available.</p>"

    else:
        forecast_html = "<p>30-day forecast has not been generated. Please generate it from the Forecasting tab.</p>"
        forecast_summary = ""
        forecast_chart_html = ""

    # ---- FULL HTML DOCUMENT ----

    html_report = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DA Agent - Final Data Analysis Report</title>
<style>
body {{ font-family: Arial, Helvetica, sans-serif; background-color: #F3F4F6; margin: 0; padding: 0; color: #1F2937; }}
.container {{ width: 92%; max-width: 1300px; margin: 30px auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
.header {{ text-align: center; border-bottom: 3px solid #1E3A8A; padding-bottom: 20px; margin-bottom: 35px; }}
.header h1 {{ color: #1E3A8A; margin-bottom: 8px; }}
.header p {{ color: #6B7280; }}
.section {{ margin-top: 40px; }}
.section h2 {{ color: #1E3A8A; border-left: 5px solid #1E3A8A; padding-left: 12px; }}
.metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 20px; }}
.metric {{ background: #F3F4F6; padding: 20px; text-align: center; border-radius: 8px; }}
.metric h3 {{ margin: 0; color: #6B7280; font-size: 14px; }}
.metric p {{ margin: 10px 0 0 0; color: #1E3A8A; font-size: 24px; font-weight: bold; }}
.data-table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }}
.data-table th {{ background: #1E3A8A; color: white; padding: 10px; text-align: left; }}
.data-table td {{ border-bottom: 1px solid #E5E7EB; padding: 9px; }}
.data-table tr:nth-child(even) {{ background: #F8FAFC; }}
.ai-box {{ background: #F3F4F6; border-left: 5px solid #1E3A8A; padding: 20px; border-radius: 8px; line-height: 1.7; }}
.summary-box {{ background: #EFF6FF; border-left: 5px solid #2563EB; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
.footer {{ text-align: center; color: #6B7280; border-top: 1px solid #E5E7EB; margin-top: 50px; padding-top: 20px; font-size: 13px; }}
@media(max-width: 800px) {{ .metrics {{ grid-template-columns: repeat(2, 1fr); }} }}
</style>
</head>
<body>
<div class="container">

    <div class="header">
        <h1>📊 DA Agent</h1>
        <p>AI-Powered Data Analysis Assistant</p>
        <p><strong>Final Data Analysis Report</strong></p>
        <p>Generated on: {report_date}</p>
    </div>

    <div class="section">
        <h2>📋 Dataset Overview</h2>
        <div class="metrics">
            <div class="metric"><h3>Total Rows</h3><p>{total_rows:,}</p></div>
            <div class="metric"><h3>Total Columns</h3><p>{total_columns:,}</p></div>
            <div class="metric"><h3>Missing Values</h3><p>{missing_values:,}</p></div>
            <div class="metric"><h3>Duplicate Rows</h3><p>{duplicate_rows:,}</p></div>
        </div>
    </div>

    <div class="section">
        <h2>🔍 Column Information</h2>
        {column_table}
    </div>

    <div class="section">
        <h2>📈 Statistical Analysis</h2>
        {statistics_html}
    </div>

    <div class="section">
        <h2>🔗 Correlation Analysis</h2>
        {correlation_html}
    </div>

    <div class="section">
        <h2>🤖 AI Business Insights</h2>
        <div class="ai-box">{ai_html}</div>
    </div>

    <div class="section">
        <h2>🔮 30-Day Sales Forecast</h2>
        {forecast_summary}
        {forecast_html}
    </div>

    <div class="section">
        <h2>📊 Historical Sales + Forecast Chart</h2>
        {forecast_chart_html}
    </div>

    <div class="footer">
        <p>Generated by DA Agent</p>
        <p>AI-Powered Data Analysis Assistant</p>
    </div>

</div>
</body>
</html>
"""

    return html_report


def generate_pdf_report(df, ai_report, forecast_result, forecast_model_slope):
    """Complete PDF report banata hai aur bytes return karta hai."""

    pdf_buffer = io.BytesIO()

    pdf = SimpleDocTemplate(
        pdf_buffer, pagesize=A4,
        rightMargin=35, leftMargin=35, topMargin=35, bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle", parent=styles["Title"], alignment=TA_CENTER,
        fontSize=22, leading=28, textColor=colors.HexColor("#1E3A8A"), spaceAfter=12
    )

    heading_style = ParagraphStyle(
        "CustomHeading", parent=styles["Heading2"],
        fontSize=16, leading=20, textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=15, spaceAfter=10
    )

    normal_style = ParagraphStyle(
        "CustomNormal", parent=styles["BodyText"],
        fontSize=9, leading=14, spaceAfter=6
    )

    story = []

    # ---- TITLE ----

    story.append(Paragraph("📊 DA Agent", title_style))
    story.append(Paragraph("AI-Powered Data Analysis Report", normal_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Spacer(1, 20))

    # ---- DATASET OVERVIEW ----

    story.append(Paragraph("Dataset Overview", heading_style))

    overview_data = [
        ["Metric", "Value"],
        ["Total Rows", f"{len(df):,}"],
        ["Total Columns", f"{len(df.columns):,}"],
        ["Missing Values", f"{df.isnull().sum().sum():,}"],
        ["Duplicate Rows", f"{df.duplicated().sum():,}"]
    ]

    overview_table = Table(overview_data, colWidths=[2.8 * inch, 2.8 * inch])
    overview_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ("PADDING", (0, 0), (-1, -1), 7)
    ]))

    story.append(overview_table)

    # ---- COLUMN INFORMATION ----

    story.append(Paragraph("Column Information", heading_style))

    column_data = [["Column", "Data Type", "Non-Null", "Missing"]]

    for column in df.columns:
        column_data.append([
            str(column)[:35], str(df[column].dtype),
            f"{df[column].count():,}", f"{df[column].isnull().sum():,}"
        ])

    column_table_pdf = Table(
        column_data, repeatRows=1,
        colWidths=[2.2 * inch, 1.5 * inch, 1.2 * inch, 1.2 * inch]
    )
    column_table_pdf.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("PADDING", (0, 0), (-1, -1), 5)
    ]))

    story.append(column_table_pdf)

    # ---- STATISTICS ----

    story.append(Paragraph("Statistical Analysis", heading_style))

    numeric_df = df.select_dtypes(include=["number"])

    if not numeric_df.empty:

        pdf_stats = numeric_df.describe().T.round(2).reset_index()
        stat_headers = [str(x) for x in pdf_stats.columns]
        stat_data = [stat_headers]

        for _, row in pdf_stats.iterrows():
            stat_data.append([str(value) for value in row.values])

        stats_table = Table(
            stat_data, repeatRows=1,
            colWidths=[1.3 * inch] + [0.75 * inch for _ in range(len(stat_headers) - 1)]
        )
        stats_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 6),
            ("PADDING", (0, 0), (-1, -1), 4)
        ]))

        story.append(stats_table)

    else:
        story.append(Paragraph("No numeric columns available.", normal_style))

    # ---- CORRELATION ----

    story.append(Paragraph("Correlation Analysis", heading_style))

    if numeric_df.shape[1] >= 2:

        corr_pdf = numeric_df.corr().round(2).reset_index()
        corr_data = [[str(col) for col in corr_pdf.columns]]

        for _, row in corr_pdf.iterrows():
            corr_data.append([str(value) for value in row.values])

        corr_table = Table(corr_data, repeatRows=1)
        corr_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 6),
            ("PADDING", (0, 0), (-1, -1), 4)
        ]))

        story.append(corr_table)

    else:
        story.append(Paragraph("Not enough numeric columns for correlation analysis.", normal_style))

    # ---- AI INSIGHTS ----

    story.append(PageBreak())
    story.append(Paragraph("AI Business Insights", heading_style))

    if ai_report:

        ai_lines = ai_report.splitlines()

        for line in ai_lines:
            clean_line = line.strip()

            if not clean_line:
                story.append(Spacer(1, 5))
                continue

            clean_line = clean_line.replace("#", "")
            story.append(Paragraph(escape(clean_line), normal_style))

    else:
        story.append(Paragraph("AI report was not generated.", normal_style))

    # ---- FORECAST ----

    story.append(Paragraph("30-Day Sales Forecast", heading_style))

    if forecast_result is not None:

        forecast_pdf = forecast_result.copy()
        forecast_data = [["Date", "Predicted Sales"]]

        for _, row in forecast_pdf.iterrows():
            forecast_data.append([
                row["Date"].strftime("%Y-%m-%d"),
                f"{row['Predicted Sales']:,.2f}"
            ])

        forecast_table_pdf = Table(
            forecast_data, repeatRows=1,
            colWidths=[2.5 * inch, 2.5 * inch]
        )
        forecast_table_pdf.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("PADDING", (0, 0), (-1, -1), 5)
        ]))

        story.append(forecast_table_pdf)
        story.append(Spacer(1, 15))

        total_forecast = forecast_result["Predicted Sales"].sum()

        story.append(Paragraph(f"Predicted Total Sales: {total_forecast:,.2f}", normal_style))
        story.append(Paragraph("Model: Linear Regression", normal_style))
        story.append(Paragraph(f"Trend/Slope: {forecast_model_slope:,.4f}", normal_style))

    else:
        story.append(Paragraph("30-day forecast was not generated.", normal_style))

    # ---- BUILD ----

    pdf.build(story)
    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()