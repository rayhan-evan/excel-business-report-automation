from src.config import DATA_DIR, OUTPUT_DIR, LOG_DIR


def test_project_directories_are_defined():
    assert DATA_DIR.name == "data"
    assert OUTPUT_DIR.name == "output"
    assert LOG_DIR.name == "logs"
