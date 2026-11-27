
import pandas as pd
from pathlib import Path

from src.config import PROJECT_ROOT


def main():
    client_dir = PROJECT_ROOT / "client_template"
    client_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "Invoice No": [
            "INV-001", "INV-002", "INV-003",
            "INV-004", "INV-005",
        ],
        "Invoice Date": [
            "2026-04-01", "2026-04-02", "2026-04-03",
            "2026-04-04", "2026-04-05",
        ],
        "Branch Name": [
            "Dhaka", "Chattogram", "Dhaka",
            "Khulna", "Chattogram",
        ],
        "Item Name": [
            "Laptop", "Mouse", "Office Chair",
            "Keyboard", "Monitor",
        ],
        "Product Category": [
            "Electronics", "Accessories", "Furniture",
            "Accessories", "Electronics",
        ],
        "Qty": [2, 5, 1, 3, 2],
        "Selling Price": [65000, 800, 8500, 1500, 18000],
        "Sales Person": [
            "Rahim", "Karim", "Nadia", "Sadia", "Tanvir",
        ],
        "Payment Type": [
            "Cash", "Card", "Mobile Banking", "Cash", "Card",
        ],
    }

    df = pd.DataFrame(data)

    output_file = client_dir / "client_sales_april.xlsx"
    df.to_excel(output_file, index=False)

    print(f"Client sample created: {output_file}")


if __name__ == "__main__":
    main()
