"""Read and consolidate multiple Excel sales workbooks."""

import logging
import re
from pathlib import Path

import pandas as pd

from src.config import DATA_DIR, SUPPORTED_INPUT_SUFFIXES

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


# Alternative column names accepted from client Excel files.
COLUMN_ALIASES = {
    "Transaction_ID": [
        "Transaction ID",
        "Transaction No",
        "Invoice ID",
        "Invoice No",
        "Order ID",
    ],
    "Order_Date": [
        "Order Date",
        "Invoice Date",
        "Transaction Date",
        "Date",
    ],
    "Branch": [
        "Branch Name",
        "Location",
        "Store",
        "Store Name",
    ],
    "Product": [
        "Product Name",
        "Item",
        "Item Name",
    ],
    "Category": [
        "Product Category",
        "Item Category",
    ],
    "Quantity": [
        "Qty",
        "Units",
        "Number of Units",
    ],
    "Unit_Price": [
        "Selling Price",
        "Unit Selling Price",
        "Sales Price",
        "Price Per Unit",
        "Price",
    ],
    "Sales_Rep": [
        "Sales Representative",
        "Sales Person",
        "Employee Name",
        "Salesperson",
    ],
    "Payment_Method": [
        "Payment Type",
        "Payment Mode",
        "Mode of Payment",
    ],
}


def normalize_column_name(column_name: str) -> str:
    """Normalize column names for reliable matching."""
    return re.sub(
        r"[^a-z0-9]",
        "",
        str(column_name).strip().lower(),
    )


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert recognized alternative column names to standard names."""

    alias_lookup = {}

    for standard_name, aliases in COLUMN_ALIASES.items():
        for alias in [standard_name, *aliases]:
            alias_lookup[normalize_column_name(alias)] = standard_name

    rename_mapping = {}

    for original_name in df.columns:
        normalized_name = normalize_column_name(original_name)

        standard_name = alias_lookup.get(normalized_name)

        if standard_name:
            rename_mapping[original_name] = standard_name

    mapped_names = list(rename_mapping.values())

    if len(mapped_names) != len(set(mapped_names)):
        raise ValueError(
            "Multiple input columns map to the same standard column. "
            "Please remove duplicate or conflicting columns."
        )

    return df.rename(columns=rename_mapping)




def read_excel_files(data_dir: Path = DATA_DIR) -> pd.DataFrame:
    """Read and consolidate supported Excel and CSV sales files."""

    if not data_dir.exists():
        raise FileNotFoundError(
            f"Input directory not found: {data_dir}"
        )

    files = sorted(
        file
        for file in data_dir.iterdir()
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_INPUT_SUFFIXES
        and not file.name.startswith("~$")
    )

    if not files:
        raise FileNotFoundError(
            f"No supported sales files (.xlsx, .csv) found in: {data_dir}"
        )

    all_data = []

    for file in files:
        logger.info("Reading sales file: %s", file.name)

        try:
            if file.suffix.lower() == ".xlsx":
                df = pd.read_excel(file, engine="openpyxl")
            elif file.suffix.lower() == ".csv":
                df = pd.read_csv(file)
            else:
                continue

        except Exception:
            logger.exception(
                "Failed to read sales file: %s",
                file.name,
            )
            raise

        df.columns = df.columns.astype(str).str.strip()

        df = standardize_columns(df)

        logger.info(
            "Standardized column names for file: %s",
            file.name,
        )

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"{file.name} is missing columns: {missing_columns}"
            )

        df["Source_File"] = file.name
        all_data.append(df)

    combined_df = pd.concat(all_data, ignore_index=True)

    logger.info(
        "Loaded %d records from %d files.",
        len(combined_df),
        len(files),
    )

    return combined_df

