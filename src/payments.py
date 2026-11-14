"""
src/payments.py
Subject Payment Calculation Module for T010-PS-126
"""

def calculate_payment(visit_name: str, travel_cost: float = 0.0):
    """Calculates total payment (stipend + travel reimbursement) for a completed visit."""
    stipend_schedule = {
        "Screening": 100.0,
        "Baseline": 250.0,
        "Follow-up": 250.0,
        "Closeout": 400.0
    }
    
    # Get stipend for visit, default to 200.0 if not listed
    stipend = stipend_schedule.get(visit_name, 200.0)
    total_payment = stipend + travel_cost
    
    return total_payment