"""
src/main.py
Main Entry Point for T010-PS-126: Clinical Trial Management Engine
"""

import sys
from src.screening import check_screening_eligibility
from src.visits import calculate_visit_window
from src.payments import calculate_payment
from src.withdrawals import process_withdrawal

def display_menu():
    print("\n==================================================")
    print("   T010-PS-126: CLINICAL TRIAL MANAGEMENT ENGINE   ")
    print("==================================================")
    print("1. Check Subject Screening Eligibility")
    print("2. Calculate Visit Windows")
    print("3. Process Subject Payment")
    print("4. Handle Subject Withdrawal")
    print("5. Exit")
    print("--------------------------------------------------")

def main():
    print("Initializing Clinical Trial Engine...")
    
    while True:
        display_menu()
        choice = input("Enter your option (1-5): ").strip()
        
        if choice == "1":
            print("\n--- Screening Eligibility Check ---")
            try:
                age = int(input("Enter subject age: ").strip())
                consent = input("Has signed informed consent? (yes/no): ").strip().lower()
                is_eligible = check_screening_eligibility(age, consent == "yes")
                if is_eligible:
                    print("[RESULT] Subject is ELIGIBLE for enrolment.")
                else:
                    print("[RESULT] Subject is NOT eligible.")
            except ValueError:
                print("[ERROR] Please enter a valid number for age.")
                
        elif choice == "2":
            print("\n--- Visit Window Calculator ---")
            baseline_date = input("Enter baseline date (YYYY-MM-DD): ").strip()
            visit_type = input("Enter visit name (e.g., Follow-up): ").strip()
            try:
                target, start, end = calculate_visit_window(baseline_date, visit_type)
                print(f"\n[RESULT] Visit: {visit_type}")
                print(f"  Target Date : {target}")
                print(f"  Window Start: {start}")
                print(f"  Window End  : {end}")
            except Exception as e:
                print(f"[ERROR] Could not calculate window: {e}")
                
        elif choice == "3":
            print("\n--- Subject Payment Calculator ---")
            visit_name = input("Enter completed visit name: ").strip()
            try:
                travel_cost = float(input("Enter travel reimbursement amount ($): ").strip() or 0.0)
                total = calculate_payment(visit_name, travel_cost)
                print(f"\n[RESULT] Total payment calculated: ${total:.2f}")
            except ValueError:
                print("[ERROR] Please enter a valid number for travel reimbursement.")
            
        elif choice == "4":
            print("\n--- Subject Withdrawal Handling ---")
            subject_id = input("Enter Subject ID: ").strip()
            reason = input("Enter withdrawal reason: ").strip()
            msg = process_withdrawal(subject_id, reason)
            print(f"\n[RESULT] {msg}")
            
        elif choice == "5":
            print("\nExiting application. Goodbye, Bindushree!")
            sys.exit(0)
        else:
            print("[ERROR] Invalid option. Please choose between 1 and 5.")

if __name__ == "__main__":
    main