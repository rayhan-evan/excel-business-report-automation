
import pandas as pd
import pytest

from src.excel_reader import read_excel_files


def create_sample_sales_data():
    return pd.DataFrame({
        "Transaction ID": ["TXN001", "TXN002"],
        "Order Date": ["2026-04-01", "2026-04-02"],
        "Branch Name": ["Dhaka", "Chittagong"],
        "Product Name": ["Laptop", "Mouse"],
        "Category": ["Electronics", "Accessories"],
        "Qty": [2, 5],
        "Selling Price": [65000, 800],
        "Sales Person": ["Rahim", "Karim"],
        "Payment Type": ["Cash", "Card"],
    })


def test_csv_file_is_read_successfully(tmp_path):
    sample_data = create_sample_sales_data()
    sample_data.to_csv(tmp_path / "sales.csv", index=False)

    result = read_excel_files(tmp_path)

    assert len(result) == 2
    assert "Transaction_ID" in result.columns
    assert "Order_Date" in result.columns
    assert result["Transaction_ID"].tolist() == ["TXN001", "TXN002"]


def test_csv_and_excel_files_are_combined(tmp_path):
    sample_data = create_sample_sales_data()

    sample_data.to_csv(tmp_path / "sales.csv", index=False)
    sample_data.to_excel(tmp_path / "sales.xlsx", index=False)

    result = read_excel_files(tmp_path)

    assert len(result) == 4
    assert result["Transaction_ID"].nunique() == 2
    assert set(result["Source_File"]) == {
        "sales.csv",
        "sales.xlsx",
    }


def test_missing_required_columns_raise_error(tmp_path):
    pd.DataFrame({
        "Transaction ID": ["TXN001"],
        "Product Name": ["Laptop"],
    }).to_csv(tmp_path / "invalid.csv", index=False)

    with pytest.raises(ValueError, match="missing columns"):
        read_excel_files(tmp_path)


def test_empty_input_directory_raises_error(tmp_path):
    with pytest.raises(FileNotFoundError, match="No supported"):
        read_excel_files(tmp_path)
