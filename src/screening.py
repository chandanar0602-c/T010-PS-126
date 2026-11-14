"""
src/screening.py
Subject Screening Eligibility Module for T010-PS-126
"""

def check_screening_eligibility(age: int, has_consent: bool) -> bool:
    """Checks if a subject meets the age (>= 18) and consent criteria."""
    if age >= 18 and has_consent:
        return True
    return False