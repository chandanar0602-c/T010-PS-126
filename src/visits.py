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