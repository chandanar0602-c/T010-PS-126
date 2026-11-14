"""
src/visits.py
Visit Window Calculation Module for T010-PS-126
"""

from datetime import datetime, timedelta

def calculate_visit_window(baseline_date_str: str, visit_type: str):
    """Calculates target date and allowable window bounds for a trial visit."""
    try:
        baseline_date = datetime.strptime(baseline_date_str.strip(), "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")

    offsets = {
        "Screening": 0,
        "Baseline": 0,
        "Follow-up": 30,
        "Closeout": 90
    }
    
    days = offsets.get(visit_type, 30)
    target_date = baseline_date + timedelta(days=days)
    window_start = target_date - timedelta(days=5)
    window_end = target_date + timedelta(days=5)
    
    return (
        target_date.strftime("%Y-%m-%d"), 
        window_start.strftime("%Y-%m-%d"), 
        window_end.strftime("%Y-%m-%d")
    )