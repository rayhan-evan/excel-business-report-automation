
"""Validate sales transactions and separate invalid records."""

import pandas as pd


REQUIRED_FIELDS = [
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


def validate_sales_data(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate transactions.

    Returns:
        valid_df: Transactions passing all validation rules.
        invalid_df: Rejected transactions with explanations.

    Duplicate transaction IDs are flagged on all occurrences.
    """

    data = df.copy()
    issues = pd.Series("", index=data.index, dtype="object")

    def add_issue(mask: pd.Series, message: str) -> None:
        """Append a validation message to affected rows."""
        nonlocal issues
        issues.loc[mask] = issues.loc[mask].apply(
            lambda current: (
                f"{current}; {message}" if current else message
            )
        )

    # Rule 1: Required fields must not be missing.
    for column in REQUIRED_FIELDS:
        add_issue(
            data[column].isna(),
            f"Missing {column}",
        )

    # Rule 2: Transaction IDs must be unique.
    duplicate_mask = (
        data["Transaction_ID"].notna()
        & data["Transaction_ID"].duplicated(keep=False)
    )
    add_issue(duplicate_mask, "Duplicate Transaction_ID")

    # Rule 3: Quantity must be greater than zero.
    add_issue(
        data["Quantity"].notna() & (data["Quantity"] <= 0),
        "Quantity must be greater than zero",
    )

    # Rule 4: Unit price must be greater than zero.
    add_issue(
        data["Unit_Price"].notna() & (data["Unit_Price"] <= 0),
        "Unit_Price must be greater than zero",
    )

    # Add validation results.
    data["Validation_Issues"] = issues

    invalid_mask = data["Validation_Issues"] != ""

    valid_df = data.loc[~invalid_mask].copy()
    invalid_df = data.loc[invalid_mask].copy()

    # Calculate revenue only for valid transactions.
    valid_df["Sales_Amount"] = (
        valid_df["Quantity"] * valid_df["Unit_Price"]
    )

    return valid_df, invalid_df