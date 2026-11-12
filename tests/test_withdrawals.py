import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from withdrawals import calculate_et_payment
from withdrawals import complete_et_visit



from withdrawals import record_withdrawal, schedule_et_visit


def test_withdrawal_and_et():

    # Test 1: Record withdrawal
    withdrawal = record_withdrawal(
        "HYD-001",
        "2026-06-10",
        "Subject requested withdrawal"
    )

    assert withdrawal["status"] == "WITHDRAWN"
    assert withdrawal["site_slot_released"] is False
    assert withdrawal["et_visit_required"] is True

    # Test 2: Schedule ET visit
    et_visit = schedule_et_visit(
        withdrawal,
        "2026-06-10"
    )

    assert et_visit["visit_code"] == "ET"
    assert et_visit["et_deadline"] == "2026-06-24"
    assert et_visit["status"] == "PENDING"

    print("All withdrawal and ET scheduling tests passed!")


if __name__ == "__main__":
    test_withdrawal_and_et()


def test_et_visit_completion():

    withdrawal = record_withdrawal(
        "HYD-002",
        "2026-06-10",
        "Subject requested withdrawal"
    )

    et_visit = schedule_et_visit(
        withdrawal,
        "2026-06-10"
    )

    # Completed within 14 days
    completed = complete_et_visit(
        et_visit,
        "2026-06-24"
    )

    assert completed["status"] == "COMPLETED"
    assert completed["within_14_days"] is True

    # Completed after 14 days
    late = complete_et_visit(
        et_visit,
        "2026-06-25"
    )

    assert late["within_14_days"] is False

    print("All ET completion tests passed!")


if __name__ == "__main__":
    test_withdrawal_and_et()
    test_et_visit_completion()


def test_et_payment():

    # Test 1: 80 km travel, capped at Rs.800
    payment = calculate_et_payment(2500, 80)

    assert payment["subject_payment"] == 2500
    assert payment["travel_reimbursement"] == 800
    assert payment["total_payment"] == 3300

    # Test 2: 20 km travel
    payment = calculate_et_payment(1500, 20)

    assert payment["travel_reimbursement"] == 200
    assert payment["total_payment"] == 1700

    print("All ET payment tests passed!")


if __name__ == "__main__":
    test_withdrawal_and_et()
    test_et_visit_completion()
    test_et_payment()

