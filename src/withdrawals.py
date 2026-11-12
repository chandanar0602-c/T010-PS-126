
from datetime import datetime


def record_withdrawal(subject_number, withdrawal_date, reason):
    """
    Record a subject withdrawal without deleting subject data.
    """

    date_value = datetime.strptime(
        withdrawal_date, "%Y-%m-%d"
    ).date()

    return {
        "subject_number": subject_number,
        "withdrawal_date": date_value.isoformat(),
        "withdrawal_reason": reason,
        "status": "WITHDRAWN",
        "et_visit_required": True,
        "site_slot_released": False
    }

from datetime import timedelta


def schedule_et_visit(withdrawal, withdrawal_date):
    """
    Schedule an Early Termination visit within 14 days
    after withdrawal.
    """

    date_value = datetime.strptime(
        withdrawal_date, "%Y-%m-%d"
    ).date()

    et_deadline = date_value + timedelta(days=14)

    return {
        "subject_number": withdrawal["subject_number"],
        "visit_code": "ET",
        "withdrawal_date": date_value.isoformat(),
        "et_deadline": et_deadline.isoformat(),
        "status": "PENDING"
    }

def complete_et_visit(et_visit, actual_date):
    """
    Record completion of an Early Termination visit.
    """

    actual = datetime.strptime(
        actual_date, "%Y-%m-%d"
    ).date()

    deadline = datetime.strptime(
        et_visit["et_deadline"], "%Y-%m-%d"
    ).date()

    return {
        **et_visit,
        "actual_date": actual.isoformat(),
        "status": "COMPLETED",
        "within_14_days": actual <= deadline
    }

def calculate_et_payment(next_visit_payment, travel_km_one_way):
    """
    Calculate subject reimbursement for an ET visit.

    ET payment uses the next scheduled protocol visit amount.
    Travel reimbursement is Rs.10 per km, capped at Rs.800.
    """

    subject_payment = float(next_visit_payment)

    travel_reimbursement = min(
        float(travel_km_one_way) * 10,
        800
    )

    return {
        "subject_payment": subject_payment,
        "travel_reimbursement": travel_reimbursement,
        "total_payment": subject_payment + travel_reimbursement
    }


