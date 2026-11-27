
"""Generate synthetic retail sales workbooks for portfolio development."""

from pathlib import Path
import random
import pandas as pd

from src.config import DATA_DIR

random.seed(42)

PRODUCTS = {
    "Laptop": ("Electronics", 65000),
    "Mobile Phone": ("Electronics", 25000),
    "Headphone": ("Accessories", 2500),
    "Keyboard": ("Accessories", 1500),
    "Office Chair": ("Furniture", 8500),
    "Desk": ("Furniture", 12000),
    "Monitor": ("Electronics", 18000),
    "Mouse": ("Accessories", 800),
}

BRANCHES = ["Dhaka", "Chattogram", "Khulna"]
SALES_REPS = ["Rahim", "Karim", "Nadia", "Sadia", "Tanvir"]
PAYMENT_METHODS = ["Cash", "Card", "Mobile Banking"]

MONTHS = [
    ("january", 1),
    ("february", 2),
    ("march", 3),
]


def generate_monthly_data(month_name: str, month_number: int) -> pd.DataFrame:
    """Generate 100 synthetic transactions for a given month."""

    records = []

    for i in range(1, 101):
        product = random.choice(list(PRODUCTS.keys()))
        category, base_price = PRODUCTS[product]

        record = {
            "Transaction_ID": f"TXN-{month_number:02d}-{i:04d}",
            "Order_Date": (
                pd.Timestamp(2026, month_number, 1)
                + pd.Timedelta(days=random.randint(0, 27))
            ).strftime("%Y-%m-%d"),
            "Branch": random.choice(BRANCHES),
            "Product": product,
            "Category": category,
            "Quantity": random.randint(1, 5),
            "Unit_Price": base_price,
            "Sales_Rep": random.choice(SALES_REPS),
            "Payment_Method": random.choice(PAYMENT_METHODS),
        }

        records.append(record)

    df = pd.DataFrame(records)

    # Introduce realistic data-quality issues.
    df.loc[5, "Product"] = None
    df.loc[10, "Sales_Rep"] = None
    df.loc[15, "Quantity"] = -2
    df.loc[20, "Quantity"] = 0
    df.loc[25, "Unit_Price"] = None
    df.loc[30, "Branch"] = "  Dhaka  "
    df.loc[35, "Product"] = "  Laptop  "
    df.loc[40, "Order_Date"] = "invalid-date"

    # Add an exact duplicate transaction.
    duplicate = df.iloc[[0]].copy()
    df = pd.concat([df, duplicate], ignore_index=True)

    return df


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for month_name, month_number in MONTHS:
        df = generate_monthly_data(month_name, month_number)

        output_file = DATA_DIR / f"sales_{month_name}.xlsx"

        df.to_excel(
            output_file,
            index=False,
            engine="openpyxl"
        )

        print(f"Created: {output_file.name} ({len(df)} records)")

    print("\nSample dataset generation completed.")


if __name__ == "__main__":
    main()