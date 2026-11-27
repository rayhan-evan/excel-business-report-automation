
import pandas as pd
import pytest

from src.excel_reader import standardize_columns


def test_alternative_columns_are_standardized():
    df = pd.DataFrame({
        "Invoice No": ["INV-001"],
        "Invoice Date": ["2026-01-15"],
        "Branch Name": ["Dhaka"],
        "Item Name": ["Laptop"],
        "Product Category": ["Electronics"],
        "Qty": [2],
        "Selling Price": [65000],
        "Sales Person": ["Rahim"],
        "Payment Type": ["Cash"],
    })

    result = standardize_columns(df)

    expected_columns = [
        "Transaction_ID",
        "Order_Date",
        "Branch",
        "Product",
        "Category",
        "Quantity",
        "Unit_Price",
        "Sales_Rep",
        "Payment_Method",
    ]

    assert list(result.columns) == expected_columns
    assert result.loc[0, "Product"] == "Laptop"
    assert result.loc[0, "Quantity"] == 2
    assert result.loc[0, "Unit_Price"] == 65000


def test_standard_column_names_remain_unchanged():
    df = pd.DataFrame({
        "Transaction_ID": ["TXN-001"],
        "Product": ["Laptop"],
        "Quantity": [2],
    })

    result = standardize_columns(df)

    assert list(result.columns) == list(df.columns)


def test_duplicate_mapped_columns_raise_error():
    df = pd.DataFrame({
        "Product": ["Laptop"],
        "Item Name": ["Keyboard"],
    })

    with pytest.raises(ValueError, match="Multiple input columns"):
        standardize_columns(df)
