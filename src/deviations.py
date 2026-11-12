def create_deviation(subject_number, visit_code, classification, detected_date):
    """
    Create a deviation record for an out-of-window or missed visit.
    """

    if classification == "OUT_OF_WINDOW":
        severity = "MINOR"

    elif classification == "MISSED":
        severity = "MAJOR"

    else:
        return None

    from datetime import datetime, timedelta

    detected = datetime.strptime(
        detected_date, "%Y-%m-%d"
    ).date()

    pi_ack_due = detected + timedelta(days=10)

    return {
        "subject_number": subject_number,
        "visit_code": visit_code,
        "severity": severity,
        "detected_date": detected.isoformat(),
        "pi_ack_due": pi_ack_due.isoformat(),
        "pi_ack_date": ""
    }

def check_pi_acknowledgement_required(deviations):
    """
    Check whether a subject requires PI acknowledgement.
    """

    minor_count = 0
    major_count = 0

    for deviation in deviations:
        if deviation["severity"] == "MINOR":
            minor_count += 1

        elif deviation["severity"] == "MAJOR":
            major_count += 1

    if minor_count > 3 or major_count > 1:
        return True

    return False

def check_site_audit_status(classified_visits):
    """
    Check whether a site exceeds the 10% major deviation threshold.

    Each visit must contain:
    - classification
    - visit_code
    """

    eligible_visits = [
        visit for visit in classified_visits
        if visit["visit_code"] in {
            "D7", "D14", "D28", "D56", "D84", "D168"
        }
        and visit["classification"] in {
            "IN_WINDOW", "OUT_OF_WINDOW", "MISSED"
        }
    ]

    total_visits = len(eligible_visits)

    if total_visits == 0:
        return "ACTIVE"

    major_deviations = sum(
        1 for visit in eligible_visits
        if visit["classification"] == "MISSED"
    )

    major_percentage = (
        major_deviations / total_visits
    ) * 100

    if major_percentage > 10:
        return "FOR_AUDIT"

    return "ACTIVE"
