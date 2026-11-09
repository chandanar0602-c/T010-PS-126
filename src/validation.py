from datetime import datetime


def validate_data(data):

    errors = []

    # 1. Validate protocol arms
    arms = data["arms"]
    arm_ids = [arm["arm_id"] for arm in arms]

    if len(arm_ids) != len(set(arm_ids)):
        errors.append("Duplicate arm IDs found")

    for arm in arms:
        try:
            ratio = float(arm["allocation_ratio"])

            if ratio <= 0:
                errors.append(
                    f"Invalid allocation ratio for {arm['arm_id']}"
                )

        except ValueError:
            errors.append(
                f"Invalid allocation ratio for {arm['arm_id']}"
            )

    # 2. Validate protocol visits
    visits = data["visits"]
    visit_codes = [visit["visit_code"] for visit in visits]

    if len(visit_codes) != len(set(visit_codes)):
        errors.append("Duplicate visit codes found")

    for visit in visits:
        try:
            day = int(visit["day_offset"])
            minus = int(visit["window_minus_days"])
            plus = int(visit["window_plus_days"])

            if day < 0 or minus < 0 or plus < 0:
                errors.append(
                    f"Invalid visit schedule for {visit['visit_code']}"
                )

        except ValueError:
            errors.append(
                f"Invalid visit schedule for {visit['visit_code']}"
            )

    # 3. Validate site registrations
    sites = data["sites"]
    site_ids = [site["site_id"] for site in sites]

    if len(site_ids) != len(set(site_ids)):
        errors.append("Duplicate site IDs found")

    for site in sites:

        try:
            cap = int(site["enrolment_cap"])

            if cap <= 0:
                errors.append(
                    f"Invalid enrolment cap for {site['site_id']}"
                )

        except ValueError:
            errors.append(
                f"Invalid enrolment cap for {site['site_id']}"
            )

        for field in ["activation_date", "irb_expiry_date"]:
            try:
                datetime.strptime(site[field], "%Y-%m-%d")

            except ValueError:
                errors.append(
                    f"Invalid {field} for site {site['site_id']}"
                )

    return errors