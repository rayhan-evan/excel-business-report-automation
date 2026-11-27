"""Read and consolidate multiple Excel sales workbooks."""

import logging
from pathlib import Path

import pandas as pd

from src.config import DATA_DIR

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
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


def read_excel_files(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """
    Read all Excel workbooks from a directory and combine them.

    Returns:
        A consolidated DataFrame containing all transactions.

    Raises:
        FileNotFoundError: If no Excel files are found.
        ValueError: If a workbook is missing required columns.
    """

    files = sorted(
        file for file in data_dir.glob("*.xlsx")
        if not file.name.startswith("~$")
    )

    if not files:
        raise FileNotFoundError(
            f"No Excel files found in: {data_dir}"
        )

    all_data = []

    for file in files:
        logger.info("Reading workbook: %s", file.name)

        df = pd.read_excel(file, engine="openpyxl")

        # Standardize column names for schema checking.
        df.columns = df.columns.astype(str).str.strip()

        missing_columns = [
            column for column in REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"{file.name} is missing columns: {missing_columns}"
            )

        # Track the source workbook for auditing.
        df["Source_File"] = file.name

        all_data.append(df)

    combined_df = pd.concat(
        all_data,
        ignore_index=True
    )

    logger.info(
        "Successfully loaded %d records from %d workbooks.",
        len(combined_df),
        len(files),
    )

    return combined_df