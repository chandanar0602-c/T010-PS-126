import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deviations import create_deviation


def test_deviation_creation():

    # Test 1: Out-of-window visit = Minor
    minor = create_deviation(
        "BLR-001",
        "D7",
        "OUT_OF_WINDOW",
        "2026-03-12"
    )

    assert minor["severity"] == "MINOR"
    assert minor["pi_ack_due"] == "2026-03-22"

    # Test 2: Missed visit = Major
    major = create_deviation(
        "BLR-002",
        "D14",
        "MISSED",
        "2026-03-20"
    )

    assert major["severity"] == "MAJOR"
    assert major["pi_ack_due"] == "2026-03-30"

    # Test 3: Normal visit creates no deviation
    normal = create_deviation(
        "BLR-003",
        "D28",
        "IN_WINDOW",
        "2026-04-01"
    )

    assert normal is None

    print("All deviation creation tests passed!")


if __name__ == "__main__":
    test_deviation_creation()


from deviations import check_pi_acknowledgement_required


def test_pi_acknowledgement_thresholds():

    # Exactly 3 minor deviations: No acknowledgement
    assert check_pi_acknowledgement_required([
        {"severity": "MINOR"},
        {"severity": "MINOR"},
        {"severity": "MINOR"}
    ]) is False

    # 4 minor deviations: Acknowledgement required
    assert check_pi_acknowledgement_required([
        {"severity": "MINOR"},
        {"severity": "MINOR"},
        {"severity": "MINOR"},
        {"severity": "MINOR"}
    ]) is True

    # Exactly 1 major deviation: No acknowledgement
    assert check_pi_acknowledgement_required([
        {"severity": "MAJOR"}
    ]) is False

    # 2 major deviations: Acknowledgement required
    assert check_pi_acknowledgement_required([
        {"severity": "MAJOR"},
        {"severity": "MAJOR"}
    ]) is True

    print("All PI acknowledgement tests passed!")

from deviations import check_site_audit_status


def test_site_audit_detection():

    # Case 1: Exactly 10% major deviations — no audit
    visits_10_percent = [
        {"visit_code": "D7", "classification": "MISSED"}
    ] + [
        {"visit_code": "D14", "classification": "IN_WINDOW"}
        for _ in range(9)
    ]

    assert check_site_audit_status(
        visits_10_percent
    ) == "ACTIVE"

    # Case 2: More than 10% — audit required
    visits_above_10 = [
        {"visit_code": "D7", "classification": "MISSED"}
    ] + [
        {"visit_code": "D14", "classification": "IN_WINDOW"}
        for _ in range(8)
    ]

    assert check_site_audit_status(
        visits_above_10
    ) == "FOR_AUDIT"

    # Case 3: ET visits must be excluded
    visits_with_et = [
        {"visit_code": "ET", "classification": "MISSED"}
    ] + [
        {"visit_code": "D7", "classification": "IN_WINDOW"}
        for _ in range(9)
    ]

    assert check_site_audit_status(
        visits_with_et
    ) == "ACTIVE"

    print("All site audit tests passed!")


if __name__ == "__main__":
    test_site_audit_detection()
