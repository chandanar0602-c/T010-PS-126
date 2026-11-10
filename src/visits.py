from datetime import datetime, timedelta


def generate_visit_calendar(randomisation, protocol_visits):
    """
    Generate planned visit dates using the randomisation date as Day 0.
    """

    randomisation_date = datetime.strptime(
        randomisation["randomisation_ts"],
        "%Y-%m-%d %H:%M:%S"
    ).date()

    calendar = []

    for visit in protocol_visits:
        day_offset = int(visit["day_offset"])
        window_minus = int(visit["window_minus_days"])
        window_plus = int(visit["window_plus_days"])

        target_date = randomisation_date + timedelta(days=day_offset)
        window_open = target_date - timedelta(days=window_minus)
        window_close = target_date + timedelta(days=window_plus)

        calendar.append({
            "subject_number": randomisation["subject_number"],
            "visit_code": visit["visit_code"],
            "target_date": target_date.isoformat(),
            "window_open": window_open.isoformat(),
            "window_close": window_close.isoformat(),
            "actual_date": "",
            "classification": "PENDING",
            "deviation": ""
        })

    return calendar
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from loader import load_all_data
from visits import generate_visit_calendar


def test_visit_calendar():
    data = load_all_data()

    randomisation = {
        "subject_number": "BLR-001",
        "randomisation_ts": "2026-03-01 10:00:00"
    }

    calendar = generate_visit_calendar(
        randomisation,
        data["visits"]
    )

    assert len(calendar) == len(data["visits"])

    for visit in calendar:
        print(visit)

    assert calendar[0]["classification"] == "PENDING"

    print("\nVisit calendar test passed!")


if __name__ == "__main__":
    test_visit_calendar()
def classify_visit(visit, actual_date=None, as_of_date=None):
    from datetime import datetime, timedelta

    window_open = datetime.strptime(
        visit["window_open"], "%Y-%m-%d"
    ).date()

    window_close = datetime.strptime(
        visit["window_close"], "%Y-%m-%d"
    ).date()

    if actual_date:
        if isinstance(actual_date, str):
            actual_date = datetime.strptime(
                actual_date, "%Y-%m-%d"
            ).date()

        if window_open <= actual_date <= window_close:
            return "IN_WINDOW"

        return "OUT_OF_WINDOW"

    if as_of_date:
        if isinstance(as_of_date, str):
            as_of_date = datetime.strptime(
                as_of_date, "%Y-%m-%d"
            ).date()

        if as_of_date > window_close + timedelta(days=7):
            return "MISSED"

    return "PENDING"