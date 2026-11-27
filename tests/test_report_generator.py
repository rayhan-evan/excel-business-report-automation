
import pandas as pd
from openpyxl import load_workbook

from src.report_generator import generate_excel_report


def test_excel_report_generation(tmp_path):
    valid_df = pd.DataFrame({
        "Transaction_ID": ["TXN-001"],
        "Branch": ["Dhaka"],
        "Product": ["Laptop"],
        "Quantity": [2],
        "Unit_Price": [65000],
        "Sales_Amount": [130000],
    })

    invalid_df = pd.DataFrame({
        "Transaction_ID": ["TXN-002"],
        "Validation_Issues": [
            "Quantity must be greater than zero"
        ],
    })

    analytics = {
        "kpis": {
            "Total_Revenue": 130000.0,
            "Total_Orders": 1,
            "Total_Units_Sold": 2,
            "Average_Order_Value": 130000.0,
        },
        "monthly_sales": pd.DataFrame({
            "Month": ["2026-01"],
            "Revenue": [130000],
            "Orders": [1],
            "Units_Sold": [2],
        }),
        "branch_sales": pd.DataFrame({
            "Branch": ["Dhaka"],
            "Revenue": [130000],
            "Orders": [1],
            "Units_Sold": [2],
        }),
        "product_sales": pd.DataFrame({
            "Product": ["Laptop"],
            "Revenue": [130000],
            "Units_Sold": [2],
        }),
    }

    output_file = tmp_path / "test_report.xlsx"

    result = generate_excel_report(
        valid_df,
        invalid_df,
        analytics,
        output_path=output_file,
    )

    assert result.exists()

    workbook = load_workbook(result)

    expected_sheets = [
        "Dashboard",
        "Clean Sales Data",
        "Invalid Transactions",
        "Validation Summary",
        "Monthly Summary",
        "Branch Analysis",
        "Product Analysis",
    ]

    summary = pd.read_excel(
        result,
        sheet_name="Validation Summary"
    )

    assert not summary.empty
    assert "Validation_Issue" in summary.columns
    assert "Occurrences" in summary.columns

    assert workbook.sheetnames == expected_sheets

    assert len(workbook["Dashboard"]._charts) == 3

    assert (
        workbook["Clean Sales Data"]["A2"].value
        == "TXN-001"
    )

    assert (
        workbook["Invalid Transactions"]["B2"].value
        == "Quantity must be greater than zero"
    )
