
from pathlib import Path

from main import parse_arguments
from src.config import DATA_DIR, OUTPUT_DIR


def test_default_command_line_arguments(monkeypatch):
    monkeypatch.setattr("sys.argv", ["main.py"])

    args = parse_arguments()

    assert args.input_dir == DATA_DIR
    assert args.output == OUTPUT_DIR / "sales_business_report.xlsx"


def test_custom_command_line_arguments(monkeypatch, tmp_path):
    input_dir = tmp_path / "client_data"
    output_file = tmp_path / "client_reports" / "report.xlsx"

    monkeypatch.setattr(
        "sys.argv",
        [
            "main.py",
            "--input-dir",
            str(input_dir),
            "--output",
            str(output_file),
        ],
    )

    args = parse_arguments()

    assert args.input_dir == input_dir
    assert args.output == output_file
