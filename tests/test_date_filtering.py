
import pandas as pd
import pytest

from src.analytics import filter_sales_by_date


@pytest.fixture
def sample_sales():
    return pd.DataFrame({
        "Transaction_ID": ["TXN-001", "TXN-002", "TXN-003", "TXN-004"],
        "Order_Date": pd.to_datetime([
            "2026-01-01",
            "2026-02-15",
            "2026-03-31",
            "2026-04-01",
        ]),
        "Sales_Amount": [1000, 2000, 3000, 4000],
    })


def test_filter_by_start_and_end_date(sample_sales):
    result = filter_sales_by_date(
        sample_sales,
        "2026-02-01",
        "2026-03-31",
    )

    assert len(result) == 2
    assert result["Transaction_ID"].tolist() == [
        "TXN-002", "TXN-003"
    ]


def test_filter_by_start_date(sample_sales):
    result = filter_sales_by_date(
        sample_sales,
        start_date="2026-03-01",
    )

    assert len(result) == 2


def test_filter_by_end_date(sample_sales):
    result = filter_sales_by_date(
        sample_sales,
        end_date="2026-02-28",
    )

    assert len(result) == 2


def test_invalid_date_range_raises_error(sample_sales):
    with pytest.raises(ValueError, match="Start date"):
        filter_sales_by_date(
            sample_sales,
            "2026-04-01",
            "2026-01-01",
        )


def test_invalid_date_format_raises_error(sample_sales):
    with pytest.raises(ValueError):
        filter_sales_by_date(
            sample_sales,
            start_date="not-a-date",
        )

def test_filter_does_not_modify_original_data(sample_sales):
    original_count = len(sample_sales)

    filter_sales_by_date(
        sample_sales,
        start_date="2026-02-01",
        end_date="2026-03-31",
    )

    assert len(sample_sales) == original_count
