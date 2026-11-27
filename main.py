
import logging

from src.config import setup_logging
from src.excel_reader import read_excel_files
from src.data_cleaner import clean_sales_data
from src.data_validator import validate_sales_data
from src.analytics import generate_sales_analytics
from src.report_generator import generate_excel_report

logger = logging.getLogger(__name__)


def main():
    setup_logging()

    print("\n======================================")
    print(" AUTOMATED EXCEL BUSINESS REPORTING")
    print("======================================")

    try:
        logger.info("Application started.")

        print("\n[1] Reading Excel files...")
        raw_data = read_excel_files()
        logger.info("Loaded %d raw records.", len(raw_data))

        print("\n[2] Cleaning sales data...")
        cleaned_data = clean_sales_data(raw_data)
        logger.info("Data cleaning completed.")

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

        if valid_data.empty:
            logger.warning("No valid transactions available.")
            print("No valid transactions available for analytics.")
            return

        print("\n[4] Generating business analytics...")
        results = generate_sales_analytics(valid_data)
        logger.info("Business analytics generated successfully.")

        print("\n[5] Generating Excel report...")
        report_path = generate_excel_report(
            valid_df=valid_data,
            invalid_df=invalid_data,
            analytics=results,
        )

        logger.info("Excel report generated: %s", report_path)
        print(f"Excel report generated: {report_path}")

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
