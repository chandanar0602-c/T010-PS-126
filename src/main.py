from loader import load_all_data
from screening import (
    check_screening_eligibility,
    check_rescreen_eligibility
)


def main():

    data = load_all_data()
    subjects = data["subjects"]

    test_cases = [
        ("SCR-0027", "SCR-0070"),
        ("SCR-0043", "SCR-0074"),
        ("SCR-0163", "SCR-0266")
    ]

    print("RESCREENING TEST")
    print("================")

    for original_id, rescreen_id in test_cases:

        original = next(
            s for s in subjects
            if s["screening_id"] == original_id
        )

        rescreen = next(
            s for s in subjects
            if s["screening_id"] == rescreen_id
        )

        original_result = check_screening_eligibility(
            original,
            data["lab_ranges"],
            data["exclusions"]
        )

        allowed, reason = check_rescreen_eligibility(
            original,
            rescreen,
            original_result,
            subjects
        )

        print(
            original_id,
            "->",
            rescreen_id,
            "|",
            "ALLOWED" if allowed else "REJECTED",
            "|",
            reason
        )


if __name__ == "__main__":
    main()