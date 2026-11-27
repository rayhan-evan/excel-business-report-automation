# Automated Excel Business Reporting System

A Python portfolio project that consolidates retail sales workbooks, validates and cleans transaction data, calculates business KPIs, and generates a formatted Excel report.

## Planned capabilities

- Read multiple `.xlsx` transaction files
- Standardize columns and data types
- Detect duplicate and invalid transactions
- Calculate revenue, orders, units sold, and average order value
- Analyze sales by month, product, and branch
- Generate an Excel workbook with summary sheets and charts
- Log processing activity and report data-quality issues

## Project status

**Starter scaffold — Stage 1.** The project structure and environment configuration are ready. Implementation will be added incrementally.

## Requirements

- Python 3.11+
- pip

## Setup (Windows PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run

The application entry point will be implemented in `main.py` during the development stages.

## Project structure

```text
excel-business-report-automation/
├── data/                  # Sample input workbooks (not private business data)
├── docs/                  # Screenshots and project documentation
├── logs/                  # Runtime logs (generated; ignored by Git)
├── output/                # Generated reports (ignored by Git)
├── src/                   # Application modules
├── tests/                 # Automated tests
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## License

MIT — see [LICENSE](LICENSE).
