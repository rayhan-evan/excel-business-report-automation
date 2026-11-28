
import argparse
import logging
from pathlib import Path

from src.config import DATA_DIR, OUTPUT_DIR, setup_logging
from src.excel_reader import read_excel_files
from src.data_cleaner import clean_sales_data
from src.data_validator import validate_sales_data
from src.analytics import (
    generate_sales_analytics,
    filter_sales_by_date,
    generate_data_quality_metrics,
)
from src.report_generator import generate_excel_report


logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Automated Excel Business Reporting System"
    )

    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DATA_DIR,
        help="Directory containing input Excel/CSV files",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_DIR / "sales_business_report.xlsx",
        help="Full path of the generated Excel report",
    )

    parser.add_argument(
        "--start-date",
        type=str,
        help="Report start date (YYYY-MM-DD)",
    )

    parser.add_argument(
        "--end-date",
        type=str,
        help="Report end date (YYYY-MM-DD)",
    )

    return parser.parse_args()


def main():
    setup_logging()
    args = parse_arguments()

    try:
        logger.info("Application started.")
        logger.info("Input directory: %s", args.input_dir)
        logger.info("Output file: %s", args.output)

        print("\n======================================")
        print(" AUTOMATED EXCEL BUSINESS REPORTING")
        print("======================================")

        # Step 1: Read input files.
        print("\n[1] Reading Excel/CSV files...")

        raw_data = read_excel_files(data_dir=args.input_dir)

        logger.info("Loaded %d raw records.", len(raw_data))

        # Step 2: Clean data.
        print("\n[2] Cleaning sales data...")

        cleaned_data = clean_sales_data(raw_data)

        logger.info("Data cleaning completed.")

        # Step 3: Validate transactions.
        print("\n[3] Validating transactions...")

        valid_data, invalid_data = validate_sales_data(cleaned_data)

        logger.info(
            "Validation completed: %d valid, %d invalid.",
            len(valid_data),
            len(invalid_data),
        )

        print(f"Total records: {len(cleaned_data)}")
        print(f"Valid transactions: {len(valid_data)}")
        print(f"Invalid transactions: {len(invalid_data)}")

        # Step 4: Calculate data quality metrics.
        # Metrics cover the complete input dataset,
        # regardless of the selected reporting date range.
        print("\n[4] Calculating data quality metrics...")

        data_quality_metrics = generate_data_quality_metrics(
            raw_df=cleaned_data,
            valid_df=valid_data,
            invalid_df=invalid_data,
        )

        logger.info(
            "Data Quality Score: %.2f%%",
            data_quality_metrics["Data_Quality_Score"],
        )

        logger.info(
            "Invalid Record Rate: %.2f%%",
            data_quality_metrics["Invalid_Rate"],
        )

        logger.info(
            "Duplicate Records: %d",
            data_quality_metrics["Duplicate_Records"],
        )

        logger.info(
            "Potential Revenue: %.2f",
            data_quality_metrics["Potential_Revenue"],
        )

        logger.info(
            "Accepted Revenue: %.2f",
            data_quality_metrics["Accepted_Revenue"],
        )

        logger.info(
            "Excluded Revenue: %.2f",
            data_quality_metrics["Excluded_Revenue"],
        )

        print(
            f"Data Quality Score: "
            f"{data_quality_metrics['Data_Quality_Score']:.2f}%"
        )
        print(
            f"Invalid Record Rate: "
            f"{data_quality_metrics['Invalid_Rate']:.2f}%"
        )
        print(
            f"Duplicate Records: "
            f"{data_quality_metrics['Duplicate_Records']}"
        )

        # Stop if no valid transactions exist.
        if valid_data.empty:
            logger.warning("No valid transactions available.")
            print("\nNo valid transactions available for analytics.")
            return

        # Step 5: Apply optional date filtering.
        print("\n[5] Applying date filters...")

        filtered_valid_data = filter_sales_by_date(
            valid_data,
            start_date=args.start_date,
            end_date=args.end_date,
        )

        if filtered_valid_data.empty:
            logger.warning(
                "No transactions found in the selected date range."
            )
            print("No transactions found in the selected date range.")
            return

        logger.info(
            "Date filtering completed. %d transactions remain.",
            len(filtered_valid_data),
        )

        # Step 6: Generate business analytics.
        print("\n[6] Generating business analytics...")

        results = generate_sales_analytics(filtered_valid_data)

        # Attach full-dataset quality metrics to the report data.
        results["data_quality"] = data_quality_metrics

        logger.info("Business analytics generated successfully.")

        # Step 7: Generate Excel report.
        print("\n[7] Generating Excel report...")

        report_path = generate_excel_report(
            valid_df=filtered_valid_data,
            invalid_df=invalid_data,
            analytics=results,
            output_path=args.output,
        )

        logger.info("Excel report generated: %s", report_path)

        print(f"\nReport generated successfully: {report_path}")

        # Display business KPIs.
        print("\n========== BUSINESS KPIs ==========")

        for name, value in results["kpis"].items():
            if isinstance(value, float):
                print(f"{name}: {value:,.2f}")
            else:
                print(f"{name}: {value:,}")

        print("\n======================================")
        print(" ANALYTICS COMPLETED SUCCESSFULLY")
        print("======================================")

        logger.info("Application completed successfully.")

    except Exception:
        logger.exception("Application failed.")
        raise


if __name__ == "__main__":
    main()