from datetime import datetime, date


def calculate_age(date_of_birth, consent_date):
    """Calculate completed age on the consent date."""

    dob = datetime.strptime(
        date_of_birth, "%Y-%m-%d"
    ).date()

    age = consent_date.year - dob.year

    if (consent_date.month, consent_date.day) < (
        dob.month, dob.day
    ):
        age -= 1

    return age


def check_screening_eligibility(subject, lab_ranges, exclusion_conditions):
    """
    Check whether a subject satisfies the screening criteria.
    Returns the screening outcome and failed criteria.
    """

    failures = []

    consent_date = datetime.strptime(
        subject["consent_ts"], "%Y-%m-%d %H:%M:%S"
    ).date()

    # 1. Age check
    age = calculate_age(
        subject["date_of_birth"], consent_date
    )

    if not 18 <= age <= 65:
        failures.append("AGE")

    # 2. BMI check
    bmi = float(subject["bmi"])

    if not 18.5 <= bmi <= 35:
        failures.append("BMI")

    # 3. Laboratory range checks
    lab_fields = {
        "HB": "lab_hb",
        "ALT": "lab_alt",
        "CREAT": "lab_creat",
        "PLT": "lab_plt"
    }

    for lab in lab_ranges:

        code = lab["lab_code"].upper()
        field = lab_fields.get(code)

        if field is None:
            continue

        value = float(subject[field])
        minimum = float(lab["min_value"])
        maximum = float(lab["max_value"])

        if not minimum <= value <= maximum:
            failures.append(code)

    # 4. Exclusion condition checks
    subject_conditions = subject["conditions"].strip()

    if subject_conditions.upper() != "NONE":
        condition_codes = {
            item.strip()
            for item in subject_conditions.split(";")
        }

        excluded_codes = {
            item["condition_code"]
            for item in exclusion_conditions
        }

        if condition_codes.intersection(excluded_codes):
            failures.append("EXCLUSION_CONDITION")

    # 5. Previous clinical trial check
    previous_trial = subject["last_trial_end_date"].strip()

    if previous_trial:
        previous_date = datetime.strptime(
            previous_trial, "%Y-%m-%d"
        ).date()

        days_since_trial = (consent_date - previous_date).days

        if 0 <= days_since_trial <= 90:
            failures.append("PREVIOUS_TRIAL")

    # Final outcome
    if failures:
        return {
            "screening_id": subject["screening_id"],
            "outcome": "SCREEN_FAILED",
            "failed_criteria": ",".join(failures)
        }

    return {
        "screening_id": subject["screening_id"],
        "outcome": "ELIGIBLE",
        "failed_criteria": "NONE"
    }
def check_rescreen_eligibility(
    original_subject,
    rescreen_subject,
    original_result,
    all_subjects
):
    """
    Check whether a subject is allowed one re-screen.
    """

    # Check whether this is linked to the original screening
    if rescreen_subject["rescreen_of"] != original_subject["screening_id"]:
        return False, "INVALID_RESCREEN_REFERENCE"

    # Only laboratory failures qualify
    lab_failure_codes = {"HB", "ALT", "CREAT", "PLT"}

    failed_criteria = set(
        original_result["failed_criteria"].split(",")
    )

    if not failed_criteria.intersection(lab_failure_codes):
        return False, "RESCREEN_NOT_ALLOWED"

    if not failed_criteria.issubset(lab_failure_codes):
        return False, "RESCREEN_NOT_ALLOWED"

    # Check whether a re-screen was already attempted
    previous_rescreens = [
        subject for subject in all_subjects
        if subject["rescreen_of"] == original_subject["screening_id"]
    ]

    if len(previous_rescreens) > 1:
        return False, "RESCREEN_LIMIT_EXCEEDED"

    # Check minimum 30-day waiting period
    from datetime import datetime

    original_date = datetime.strptime(
        original_subject["consent_ts"],
        "%Y-%m-%d %H:%M:%S"
    ).date()

    rescreen_date = datetime.strptime(
        rescreen_subject["consent_ts"],
        "%Y-%m-%d %H:%M:%S"
    ).date()

    days_between = (rescreen_date - original_date).days

    if days_between < 30:
        return False, "RESCREEN_TOO_EARLY"

    return True, "RESCREEN_ALLOWED"