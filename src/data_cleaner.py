
"""Standardize and clean consolidated sales data."""

import pandas as pd


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize sales data without deleting invalid records.

    Operations:
    - Standardize column names.
    - Trim unnecessary whitespace.
    - Normalize text fields.
    - Convert dates and numeric fields.
    """

    cleaned_df = df.copy()

    # Standardize column names.
    cleaned_df.columns = (
        cleaned_df.columns.astype(str).str.strip()
    )

    # Clean text columns.
    text_columns = [
        "Transaction_ID",
        "Branch",
        "Product",
        "Category",
        "Sales_Rep",
        "Payment_Method",
    ]

    for column in text_columns:
        cleaned_df[column] = (
            cleaned_df[column]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    # Standardize branch and payment method names.
    cleaned_df["Branch"] = (
        cleaned_df["Branch"].str.title()
    )

    cleaned_df["Payment_Method"] = (
        cleaned_df["Payment_Method"].str.title()
    )

    # Convert date values.
    cleaned_df["Order_Date"] = pd.to_datetime(
        cleaned_df["Order_Date"],
        errors="coerce"
    )

    # Convert numeric values.
    cleaned_df["Quantity"] = pd.to_numeric(
        cleaned_df["Quantity"],
        errors="coerce"
    )

    cleaned_df["Unit_Price"] = pd.to_numeric(
        cleaned_df["Unit_Price"],
        errors="coerce"
    )

    return cleaned_df