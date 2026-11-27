
"""Main entry point for Excel Business Reporting System."""

import logging

from src.excel_reader import read_excel_files
from src.data_cleaner import clean_sales_data
from src.data_validator import validate_sales_data
from src.analytics import generate_sales_analytics
from src.report_generator import generate_excel_report


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    print("\n======================================")
    print(" AUTOMATED EXCEL BUSINESS REPORTING")
    print("======================================")

    # Stage 1: Read Excel files.
    print("\n[1] Reading Excel files...")

    raw_data = read_excel_files()

    print(f"Total records loaded: {len(raw_data)}")

    # Stage 2: Clean data.
    print("\n[2] Cleaning sales data...")

    cleaned_data = clean_sales_data(raw_data)

    print(f"Records processed: {len(cleaned_data)}")

    # Stage 3: Validate data.
    print("\n[3] Validating transactions...")

    valid_data, invalid_data = validate_sales_data(
        cleaned_data
    )

    print(f"Valid transactions: {len(valid_data)}")
    print(f"Invalid transactions: {len(invalid_data)}")

    # Stage 4: Business analytics.
    print("\n[4] Generating business analytics...")

    if valid_data.empty:
        print("No valid transactions available for analytics.")
        return

    results = generate_sales_analytics(valid_data)

        # Stage 5: Generate Excel report.
    print("\n[5] Generating Excel report...")

    report_path = generate_excel_report(
        valid_df=valid_data,
        invalid_df=invalid_data,
        analytics=results,
    )

    print(f"Excel report generated: {report_path}")

    print("\n========== BUSINESS KPIs ==========")

    for name, value in results["kpis"].items():
        print(f"{name}: {value:,.2f}" if isinstance(
            value, float
        ) else f"{name}: {value:,}")

    print("\n========== BRANCH PERFORMANCE ==========")
    print(results["branch_sales"].to_string(index=False))

    print("\n========== TOP 5 PRODUCTS ==========")
    print(
        results["product_sales"]
        .head(5)
        .to_string(index=False)
    )

    print("\n======================================")
    print(" ANALYTICS COMPLETED SUCCESSFULLY")
    print("======================================")


if __name__ == "__main__":
    main()
