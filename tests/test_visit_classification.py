import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from visits import classify_visit


def test_visit_classification():
    visit = {
        "window_open": "2026-03-06",
        "window_close": "2026-03-10"
    }

    # Case 1: Within the allowed window
    assert classify_visit(
        visit, actual_date="2026-03-08"
    ) == "IN_WINDOW"

    # Case 2: Outside the allowed window
    assert classify_visit(
        visit, actual_date="2026-03-11"
    ) == "OUT_OF_WINDOW"

    # Case 3: Exactly 7 days after window close
    assert classify_visit(
        visit, actual_date="2026-03-17"
    ) == "OUT_OF_WINDOW"

    # Case 4: Grace period has not expired
    assert classify_visit(
        visit, as_of_date="2026-03-17"
    ) == "PENDING"

    # Case 5: Grace period has expired
    assert classify_visit(
        visit, as_of_date="2026-03-18"
    ) == "MISSED"

    print("All 5 visit classification tests passed!")


if __name__ == "__main__":
    test_visit_classification()