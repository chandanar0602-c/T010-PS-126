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