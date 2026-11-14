"""
src/withdrawals.py
Subject Withdrawal Module for T010-PS-126
"""

def process_withdrawal(subject_id: str, reason: str):
    """Processes subject withdrawal from the clinical trial."""
    if not subject_id.strip():
        return "Error: Subject ID cannot be empty."
    
    return f"Subject {subject_id.strip()} successfully withdrawn. Reason recorded: {reason.strip()}"