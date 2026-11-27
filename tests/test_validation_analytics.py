
import pandas as pd

from src.data_validator import validate_sales_data
from src.analytics import generate_sales_analytics


def sample_data():
    return pd.DataFrame({
        "Transaction_ID": ["TXN-001", "TXN-002", "TXN-003"],
        "Order_Date": pd.to_datetime([
            "2026-01-01",
            "2026-01-02",
            "2026-01-03",
        ]),
        "Branch": ["Dhaka", "Khulna", "Dhaka"],
        "Product": ["Laptop", "Mouse", "Mobile Phone"],
        "Category": ["Electronics", "Accessories", "Electronics"],
        "Quantity": [2, 3, 1],
        "Unit_Price": [65000, 800, 25000],
        "Sales_Rep": ["Rahim", "Karim", "Nadia"],
        "Payment_Method": ["Cash", "Card", "Mobile Banking"],
    })


def test_valid_transactions_are_preserved():
    valid, invalid = validate_sales_data(sample_data())

    assert len(valid) == 3
    assert len(invalid) == 0


def test_duplicate_transactions_are_flagged():
    df = sample_data()

    duplicate = df.iloc[[0]].copy()
    df = pd.concat([df, duplicate], ignore_index=True)

    valid, invalid = validate_sales_data(df)

    assert len(valid) == 2
    assert len(invalid) == 2
    assert invalid["Validation_Issues"].str.contains(
        "Duplicate Transaction_ID"
    ).all()


def test_invalid_quantity_is_flagged():
    df = sample_data()
    df.loc[0, "Quantity"] = -2

    valid, invalid = validate_sales_data(df)

    assert len(valid) == 2
    assert len(invalid) == 1
    assert "Quantity must be greater than zero" in (
        invalid.iloc[0]["Validation_Issues"]
    )


def test_sales_kpis():
    valid, _ = validate_sales_data(sample_data())

    result = generate_sales_analytics(valid)
    kpis = result["kpis"]

    assert kpis["Total_Revenue"] == 157400
    assert kpis["Total_Orders"] == 3
    assert kpis["Total_Units_Sold"] == 6
    assert round(kpis["Average_Order_Value"], 2) == 52466.67


def test_branch_and_product_analytics():
    valid, _ = validate_sales_data(sample_data())

    result = generate_sales_analytics(valid)

    assert len(result["branch_sales"]) == 2
    assert len(result["product_sales"]) == 3
    assert result["branch_sales"].iloc[0]["Branch"] == "Dhaka"
