"""
Streamlit dashboard:
streamlit run dashboard/app.py
"""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api.services import check_database, compute_metrics, get_model_info
from dashboard.data import load_daily_metrics, load_pipeline_logs, load_predictions

st.set_page_config(
    page_title="Sales Forecast Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sales Forecast Dashboard")
st.caption("ETL + ML pipeline — daily metrics and predictions")


@st.cache_data(ttl=60)
def get_data():
    return {
        "daily": load_daily_metrics(),
        "predictions": load_predictions(),
        "logs": load_pipeline_logs(),
    }


def render_kpis(daily: pd.DataFrame) -> None:
    if daily.empty:
        st.warning("No data in daily_metrics. Run: python etl/run_etl.py")
        return

    total_sales = daily["total_sales"].sum()
    total_profit = daily["total_profit"].sum()
    avg_order = daily["avg_order_value"].mean()
    total_days = len(daily)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sales", f"{total_sales:,.0f}")
    c2.metric("Total Profit", f"{total_profit:,.0f}")
    c3.metric("Avg Order Value", f"{avg_order:,.0f}")
    c4.metric("Days Tracked", f"{total_days}")


def render_sales_chart(daily: pd.DataFrame) -> None:
    st.subheader("Daily Sales Trend")
    if daily.empty:
        return

    fig = px.line(
        daily,
        x="metric_date",
        y="total_sales",
        title="Total Sales by Day",
        labels={"metric_date": "Date", "total_sales": "Sales"},
    )
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)


def render_profit_chart(daily: pd.DataFrame) -> None:
    st.subheader("Daily Profit")
    if daily.empty:
        return

    fig = px.bar(
        daily.tail(30),
        x="metric_date",
        y="total_profit",
        title="Profit — Last 30 Days",
        labels={"metric_date": "Date", "total_profit": "Profit"},
    )
    st.plotly_chart(fig, use_container_width=True)


def render_prediction_chart(predictions: pd.DataFrame) -> None:
    st.subheader("Prediction vs Actual")
    if predictions.empty:
        st.info("No predictions yet. Run: python ml/run_ml.py")
        return

    chart_df = predictions.melt(
        id_vars=["predict_date"],
        value_vars=["predicted_sales", "actual_sales"],
        var_name="type",
        value_name="sales",
    )
    chart_df["type"] = chart_df["type"].map(
        {
            "predicted_sales": "Predicted",
            "actual_sales": "Actual",
        }
    )

    fig = px.line(
        chart_df,
        x="predict_date",
        y="sales",
        color="type",
        title="Model Predictions vs Actual Sales",
        labels={"predict_date": "Date", "sales": "Sales"},
    )
    st.plotly_chart(fig, use_container_width=True)

    error = (predictions["predicted_sales"] - predictions["actual_sales"]).abs().mean()
    st.caption(f"Average absolute error on chart: {error:,.2f}")


def render_ml_metrics() -> None:
    st.subheader("ML Metrics")
    model_info = get_model_info()

    if not model_info["loaded"]:
        st.warning("Model not found. Run: python ml/run_ml.py")
        return

    try:
        metrics = compute_metrics()
    except Exception as e:
        st.error(str(e))
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("MAE", f"{metrics['mae']:,.2f}")
    c2.metric("RMSE", f"{metrics['rmse']:,.2f}")
    c3.metric("Model Version", metrics["model_version"])
    st.caption(f"Evaluated on {metrics['test_rows']} test days")


def render_logs(logs: pd.DataFrame) -> None:
    st.subheader("Pipeline Logs")
    if logs.empty:
        st.info("No pipeline logs yet.")
        return
    st.dataframe(logs, use_container_width=True, hide_index=True)


def main() -> None:
    with st.sidebar:
        st.header("Status")
        db_ok = check_database()
        model_info = get_model_info()

        st.write("Database:", "✅ Connected" if db_ok else "❌ Error")
        st.write("Model:", "✅ Loaded" if model_info["loaded"] else "❌ Not found")
        if model_info["version"]:
            st.write("Version:", model_info["version"])

        if st.button("Refresh data"):
            get_data.clear()
            st.rerun()

        st.divider()
        st.markdown("**Commands**")
        st.code("python etl/run_etl.py")
        st.code("python ml/run_ml.py")
        st.code("uvicorn api.main:app --reload")

    data = get_data()
    daily = data["daily"]
    predictions = data["predictions"]
    logs = data["logs"]

    render_kpis(daily)

    st.divider()
    left, right = st.columns(2)
    with left:
        render_sales_chart(daily)
    with right:
        render_profit_chart(daily)

    st.divider()
    render_prediction_chart(predictions)

    st.divider()
    render_ml_metrics()

    st.divider()
    render_logs(logs)


if __name__ == "__main__":
    main()
