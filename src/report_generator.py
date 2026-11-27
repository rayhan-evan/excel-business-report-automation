
"""Generate a formatted Excel business reporting workbook."""

from pathlib import Path

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference

from src.config import OUTPUT_DIR


def build_validation_summary(invalid_df: pd.DataFrame) -> pd.DataFrame:
    """Count rejected transactions by validation issue."""

    if invalid_df.empty:
        return pd.DataFrame(columns=["Validation_Issue", "Occurrences"])

    issue_counts = (
        invalid_df["Validation_Issues"]
        .dropna()
        .str.split("; ")
        .explode()
        .value_counts()
        .rename_axis("Validation_Issue")
        .reset_index(name="Occurrences")
    )

    return issue_counts


def generate_excel_report(
    valid_df: pd.DataFrame,
    invalid_df: pd.DataFrame,
    analytics: dict,
    output_path: Path | None = None,
) -> Path:
    """Generate an Excel workbook containing six report worksheets."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if output_path is None:
        output_path = OUTPUT_DIR / "sales_business_report.xlsx"

    # Write the data worksheets.
    with pd.ExcelWriter(
        output_path,
        engine="openpyxl"
    ) as writer:

        valid_df.to_excel(
            writer,
            sheet_name="Clean Sales Data",
            index=False
        )

        invalid_df.to_excel(
            writer,
            sheet_name="Invalid Transactions",
            index=False
        )

        build_validation_summary(invalid_df).to_excel(
            writer,
            sheet_name="Validation Summary",
            index=False,
)

        analytics["monthly_sales"].to_excel(
            writer,
            sheet_name="Monthly Summary",
            index=False
        )

        analytics["branch_sales"].to_excel(
            writer,
            sheet_name="Branch Analysis",
            index=False
        )

        analytics["product_sales"].to_excel(
            writer,
            sheet_name="Product Analysis",
            index=False
        )

    workbook = load_workbook(output_path)

    # Create the executive dashboard.
    dashboard = workbook.create_sheet(
        "Dashboard",
        index=0
    )

    dashboard.sheet_view.showGridLines = False

    dashboard.merge_cells("A1:L2")
    dashboard["A1"] = "RETAIL SALES - EXECUTIVE DASHBOARD"
    dashboard["A1"].font = Font(
        name="Arial",
        size=18,
        bold=True,
        color="FFFFFF"
    )
    dashboard["A1"].fill = PatternFill(
        "solid",
        fgColor="17365D"
    )
    dashboard["A1"].alignment = Alignment(
        horizontal="center",
        vertical="center"
    )

    kpis = analytics["kpis"]

    # KPI cards.
    cards = [
        ("A4:C4", "A5:C6", "TOTAL REVENUE",
         kpis["Total_Revenue"]),
        ("E4:G4", "E5:G6", "TOTAL ORDERS",
         kpis["Total_Orders"]),
        ("I4:K4", "I5:K6", "UNITS SOLD",
         kpis["Total_Units_Sold"]),
    ]

    for label_range, value_range, label, value in cards:
        dashboard.merge_cells(label_range)
        dashboard.merge_cells(value_range)

        label_cell = dashboard[label_range.split(":")[0]]
        value_cell = dashboard[value_range.split(":")[0]]

        label_cell.value = label
        value_cell.value = value

        label_cell.font = Font(
            bold=True,
            color="FFFFFF",
            size=11
        )
        label_cell.fill = PatternFill(
            "solid",
            fgColor="4472C4"
        )
        label_cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

        value_cell.font = Font(
            bold=True,
            size=17,
            color="17365D"
        )
        value_cell.fill = PatternFill(
            "solid",
            fgColor="D9EAF7"
        )
        value_cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

        if label == "TOTAL REVENUE":
            value_cell.number_format = '"৳"#,##0.00'

    # Add average order value.
    dashboard["A7"] = "Average Order Value:"
    dashboard["A7"].font = Font(bold=True)
    dashboard["B7"] = kpis["Average_Order_Value"]
    dashboard["B7"].number_format = '"৳"#,##0.00'

    dashboard["E7"] = "Invalid Transactions:"
    dashboard["E7"].font = Font(bold=True)
    dashboard["F7"] = len(invalid_df)

    # Create Excel charts.
    chart_config = [
        ("Monthly Summary", "Monthly Revenue", "A9"),
        ("Branch Analysis", "Branch Revenue", "G9"),
        ("Product Analysis", "Product Revenue", "A25"),
    ]

    for sheet_name, chart_title, anchor in chart_config:
        source_sheet = workbook[sheet_name]

        chart = BarChart()
        chart.type = "col"
        chart.style = 10
        chart.title = chart_title
        chart.y_axis.title = "Revenue (BDT)"
        chart.x_axis.title = (
            "Month" if sheet_name == "Monthly Summary"
            else "Branch" if sheet_name == "Branch Analysis"
            else "Product"
        )
        chart.height = 8
        chart.width = 15

        data = Reference(
            source_sheet,
            min_col=2,
            min_row=1,
            max_row=source_sheet.max_row
        )

        categories = Reference(
            source_sheet,
            min_col=1,
            min_row=2,
            max_row=source_sheet.max_row
        )

        chart.add_data(data, titles_from_data=True)
        chart.set_categories(categories)

        dashboard.add_chart(chart, anchor)

    # Format all report data worksheets.
    header_fill = PatternFill(
        "solid",
        fgColor="17365D"
    )

    header_font = Font(
        bold=True,
        color="FFFFFF"
    )

    thin_border = Border(
        bottom=Side(style="thin", color="D9E2F3")
    )

    for sheet in workbook.worksheets:
        if sheet.title == "Dashboard":
            continue

        sheet.freeze_panes = "A2"
        sheet.sheet_view.showGridLines = False

        # Format headers.
        for cell in sheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(
                horizontal="center"
            )

        # Apply filters.
        sheet.auto_filter.ref = sheet.dimensions

        # Set readable column widths.
        for column_cells in sheet.columns:
            column_letter = column_cells[0].column_letter

            max_length = max(
                len(str(cell.value or ""))
                for cell in column_cells
            )

            sheet.column_dimensions[column_letter].width = min(
                max(max_length + 3, 12),
                35
            )

        # Add subtle row borders.
        for row in sheet.iter_rows(min_row=2):
            for cell in row:
                cell.border = thin_border

        # Format revenue and price columns.
        for column_cells in sheet.columns:
            header = str(column_cells[0].value)

            if header in ("Sales_Amount", "Unit_Price", "Revenue"):
                for cell in column_cells[1:]:
                    cell.number_format = '"৳"#,##0.00'

    dashboard.column_dimensions["A"].width = 19
    dashboard.column_dimensions["B"].width = 16
    dashboard.column_dimensions["E"].width = 19
    dashboard.column_dimensions["F"].width = 16
    dashboard.column_dimensions["I"].width = 19
    dashboard.column_dimensions["J"].width = 16

    dashboard.freeze_panes = "A4"

    try:
        workbook.save(output_path)
    except PermissionError as exc:
        raise PermissionError(
                f"Cannot save report to '{output_path}'. "
                "Please close the Excel workbook if it is already open, "
                "then run the application again."
            ) from exc

    return output_path
