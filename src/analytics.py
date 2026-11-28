
"""Calculate business KPIs and sales performance analytics."""

import pandas as pd
from datetime import date


def filter_sales_by_date(
    df: pd.DataFrame,
    start_date: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Filter sales transactions using an inclusive date range."""

    filtered_df = df.copy()

    if start_date:
        start = pd.to_datetime(start_date, errors="raise")
        filtered_df = filtered_df[
            filtered_df["Order_Date"] >= start
        ]

    if end_date:
        end = pd.to_datetime(end_date, errors="raise")
        filtered_df = filtered_df[
            filtered_df["Order_Date"] < end + pd.Timedelta(days=1)
        ]

    if start_date and end_date:
        if pd.to_datetime(start_date) > pd.to_datetime(end_date):
            raise ValueError(
                "Start date cannot be later than end date."
            )

    return filtered_df.copy()



def generate_sales_analytics(
    df: pd.DataFrame,
) -> dict:
    """
    Generate sales KPIs and grouped business summaries.

    Input must contain validated transactions with Sales_Amount.
    """

    if df.empty:
        raise ValueError(
            "Cannot generate analytics: no valid transactions found."
        )

    data = df.copy()

    # Overall KPIs.
    total_revenue = data["Sales_Amount"].sum()
    total_orders = data["Transaction_ID"].nunique()
    total_units = data["Quantity"].sum()

    average_order_value = (
        total_revenue / total_orders
        if total_orders else 0
    )

    kpis = {
        "Total_Revenue": round(float(total_revenue), 2),
        "Total_Orders": int(total_orders),
        "Total_Units_Sold": int(total_units),
        "Average_Order_Value": round(
            float(average_order_value), 2
        ),
    }

    # Monthly sales performance.
    data["Month"] = (
        data["Order_Date"].dt.to_period("M").astype(str)
    )

    monthly_sales = (
        data.groupby("Month", as_index=False)
        .agg(
            Revenue=("Sales_Amount", "sum"),
            Orders=("Transaction_ID", "nunique"),
            Units_Sold=("Quantity", "sum"),
        )
        .sort_values("Month")
    )

    # Branch performance.
    branch_sales = (
        data.groupby("Branch", as_index=False)
        .agg(
            Revenue=("Sales_Amount", "sum"),
            Orders=("Transaction_ID", "nunique"),
            Units_Sold=("Quantity", "sum"),
        )
        .sort_values("Revenue", ascending=False)
    )

    # Product performance.
    product_sales = (
        data.groupby("Product", as_index=False)
        .agg(
            Revenue=("Sales_Amount", "sum"),
            Units_Sold=("Quantity", "sum"),
        )
        .sort_values("Revenue", ascending=False)
    )

    return {
        "kpis": kpis,
        "monthly_sales": monthly_sales,
        "branch_sales": branch_sales,
        "product_sales": product_sales,
    }