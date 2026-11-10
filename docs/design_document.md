T010-PS-126: Clinical Trial Site Enrolment, Visit Window and Subject Payment Engine

1. Project Overview

1.1 Project Title

Clinical Trial Site Enrolment, Visit Window and Subject Payment Engine.

1.2 Team Details

- Team ID: T010
- Team Members: Chandana R and Bindushree
- Technology: Python 3.10+
- Project Domain: Clinical Research

1.3 Problem Description

Clinical trials involve multiple research sites, subjects, screening activities, randomisation, scheduled visits, deviations and payments.

Managing these activities requires careful validation of clinical trial protocols and business rules. Errors in enrolment, visit scheduling, deviation tracking or payment calculations can affect the accuracy of trial operations.

This project develops a command-file-driven engine that processes clinical trial events, enforces protocol rules and generates structured CSV reports.

1.4 Project Objectives

1. Load and validate clinical trial protocol information.
2. Register research sites and manage enrolment limits.
3. Screen subjects based on inclusion and exclusion criteria.
4. Randomise eligible subjects using block randomisation and stratification.
5. Schedule visits and classify visit completion.
6. Track protocol deviations and PI acknowledgements.
7. Manage subject withdrawals and early termination visits.
8. Calculate subject reimbursements and site payments.
9. Manage queries, payment deductions and holdbacks.
10. Generate the required output CSV reports and error logs.

1.5 Project Scope

The system processes input CSV files and commands from a text file. It maintains trial state while processing commands in order and generates six required output files.

The system does not require a graphical user interface.

2. System Architecture

2.1 Architecture Overview

The system follows a modular architecture. Each module handles a specific responsibility, while the main program coordinates the complete execution.

The engine reads input data, processes commands sequentially, applies business rules and generates the required output CSV files.

2.2 System Processing Flow

1. Load protocol information.
2. Load laboratory ranges and exclusion conditions.
3. Load research site information.
4. Load block randomisation sequences.
5. Load subject screening records.
6. Read and process commands from commands.txt in order.
7. Validate each command against the applicable business rules.
8. Update the trial state when a command is accepted.
9. Record rejected commands in errors.csv.
10. Generate the required output reports.

2.3 Module Design

Module| Responsibility
main.py| Entry point and overall coordination
loader.py| Loading and validating input CSV files
screening.py| Subject eligibility and screening decisions
randomisation.py| Stratification, block allocation and subject numbering
visits.py| Visit scheduling, classification and withdrawal-related visit handling
deviations.py| Deviation tracking, PI acknowledgement and site audit checks
payments.py| Subject reimbursement, site payments, deductions and settlement

2.4 Input Files

The system uses the following input files:

1. protocol_arms.csv
2. protocol_visits.csv
3. lab_ranges.csv
4. exclusion_conditions.csv
5. sites.csv
6. block_sequences.csv
7. subjects.csv
8. commands.txt

2.5 Output Files

The system generates six output files:

1. screening_outcomes.csv
2. randomisations.csv
3. visit_calendar.csv
4. deviation_log.csv
5. payment_statements.csv
6. errors.csv

2.6 Technology Stack

- Programming Language: Python 3.10+
- Data Processing: Python CSV handling
- Automated Testing: pytest
- Development Environment: Visual Studio Code
- Version Control: Git and GitHub

3. Data Design

3.1 Overview

The system uses structured CSV files as input and maintains application data while processing commands.

Each input file has a specific purpose and contains information required for clinical trial operations.

3.2 Protocol Data

Protocol information is loaded from:

- protocol_arms.csv
- protocol_visits.csv
- lab_ranges.csv
- exclusion_conditions.csv

This information defines treatment arms, visit schedules, visit windows, laboratory eligibility ranges and exclusion conditions.

3.3 Site Data

The sites.csv file contains:

- Site ID
- Site name
- City
- Enrolment cap
- Activation date
- IRB expiry date
- Principal Investigator name

The system uses this information to validate site eligibility and enrolment limits.

3.4 Subject Data

The subjects.csv file contains:

- Screening ID
- Site ID
- Consent timestamp
- Sex
- Date of birth
- BMI
- Laboratory values
- Medical conditions
- Previous trial end date
- One-way travel distance
- Re-screen reference

These details are used for screening, stratification, randomisation and reimbursement calculations.

3.5 Randomisation Data

The block_sequences.csv file stores the predefined treatment allocation sequence.

The system uses four strata:

- M_LT45
- M_GE45
- F_LT45
- F_GE45

Block randomisation uses a block size of four. The assigned treatment arm is selected from the next available position in the corresponding stratum sequence.

3.6 Visit Data

The system maintains visit information for each successfully randomised subject.

Visit information includes:

- Subject number
- Visit code
- Target date
- Window opening date
- Window closing date
- Actual visit date
- Visit classification
- Deviation information

Visit target dates and windows are calculated from the randomisation date according to the protocol.

3.7 Payment Data

The system maintains payment information for subjects and research sites.

Payment information includes:

- Payee type
- Payee ID
- Payment month
- Gross amount
- Applicable reductions
- Query deductions
- Holdback
- TDS
- Withheld amount
- Net payment

The payment module applies the payment rules defined by the project specification.

4. Business Rules and Validation Logic

4.1 Protocol Loading and Validation (BR-01)

- The system must load protocol arms and visit schedules.
- Laboratory reference ranges and exclusion conditions must be loaded.
- Required input data must be available before processing dependent commands.
- Invalid input data must be handled through validation.

4.2 Subject Screening and Eligibility (BR-02)

A subject must satisfy the following inclusion criteria:

- Age must be between 18 and 65 years, inclusive.
- BMI must be between 18.5 and 35, inclusive.
- All required laboratory values must fall within their configured inclusive ranges.
- The subject must not have any listed exclusion condition.
- The subject must not have participated in another clinical trial within the previous 90 days.

If any eligibility criterion fails, the screening outcome is SCREEN_FAILED.

A subject may be re-screened once after at least 30 days if the original failure was due to a laboratory value.

4.3 Subject Randomisation (BR-03)

- Only eligible subjects can be randomised.
- Randomisation must occur within 14 days of consent, inclusive.
- The system must enforce site and overall trial enrolment caps.
- Subjects are classified into four strata based on sex and age.
- Block randomisation uses block size four and the supplied block sequences.
- Subject numbers are assigned sequentially within each site.
- Site restrictions, including IRB hold and audit status, must be checked before randomisation.

4.4 Visit Scheduling and Classification (BR-04)

- Day 0 is the subject's randomisation date.
- Follow-up visits are scheduled on days 7, 14, 28, 56, 84 and 168.
- Visit windows are calculated using the protocol schedule.
- Target dates are calculated from Day 0, not from previous actual visit dates.
- Completed visits are classified as IN_WINDOW or OUT_OF_WINDOW.
- Pending visits are classified as MISSED after the specified grace period.
- Two consecutive missed visits result in LOST_TO_FOLLOW_UP.
- Visits cannot be recorded before the previous visit's window opens.
Visit Schedule and Window Rules

Day 0 is the randomisation date. All visit target dates and visit windows are calculated from Day 0.

Visit Code| Day Offset| Window Before| Window After| Allowed Visit Window
D7| 7| 2 days| 2 days| Day 5 to Day 9
D14| 14| 2 days| 2 days| Day 12 to Day 16
D28| 28| 3 days| 3 days| Day 25 to Day 31
D56| 56| 5 days| 5 days| Day 51 to Day 61
D84| 84| 7 days| 7 days| Day 77 to Day 91
D168| 168| 14 days| 21 days| Day 154 to Day 189

Visit Classification Rules:

1. A completed visit within the allowed window is classified as "IN_WINDOW".
2. A completed visit outside the allowed window is classified as "OUT_OF_WINDOW".
3. A pending visit is classified as "MISSED" when the current command date is later than the window closing date plus 7 days.
4. A visit recorded exactly on the seventh grace day is classified as "OUT_OF_WINDOW", not "MISSED".
5. All visit windows are calculated from the original randomisation date, not from the previous actual visit date.
6. A visit cannot be recorded before the previous visit's window opening date.

4.5 Deviation Management (BR-05)

- OUT_OF_WINDOW visits generate minor deviations.
- MISSED visits generate major deviations.
- More than three minor deviations or more than one major deviation per subject require PI acknowledgement within 10 days.
- The system records deviation severity, detection date and PI acknowledgement details.
- A site with major deviations exceeding 10% of its classified protocol visits is marked FOR_AUDIT at MONTH_END.
- New randomisations at an audit site are paused until CAPA is completed.

4.6 Withdrawal and Early Termination (BR-06)

- A subject may withdraw at any time.
- An Early Termination visit must occur within 14 days of withdrawal.
- Previously collected subject data is retained.
- Withdrawal does not release the subject's enrolment slot.

4.7 Subject Reimbursement (BR-07)

- Subject payments depend on the completed visit and the protocol payment schedule.
- OUT_OF_WINDOW visits remain eligible for subject reimbursement.
- MISSED visits do not receive subject reimbursement.
- Travel reimbursement is calculated at Rs 10 per kilometre, one way, subject to a maximum of Rs 800 per visit.
- Early Termination visits receive the amount assigned to the next scheduled visit.
Subject Payment Amounts and Rules

The subject payment amounts are defined as follows:

Visit| Subject Payment
D7| ₹1,500
D14| ₹1,500
D28| ₹1,500
D56| ₹2,500
D84| ₹2,500
D168| ₹2,500
Early Termination (ET)| Amount of the next scheduled visit

Subject Reimbursement Rules:

1. Payments are provided only for completed protocol visits classified as "IN_WINDOW" or "OUT_OF_WINDOW".
2. Missed visits are not eligible for subject payment.
3. Travel reimbursement is ₹10 per kilometre for one-way travel.
4. Travel reimbursement is capped at ₹800 per visit.
5. Travel reimbursement applies to protocol visits and Early Termination visits only.
6. Early Termination visits receive the payment amount of the next scheduled visit.
7. Subject payments are tax-free up to ₹50,000 per subject per financial year. Amounts exceeding this limit must be flagged.

4.8 Site Payments (BR-08)

- Site payments are calculated according to the protocol payment schedule.
- OUT_OF_WINDOW visits receive 80% of the normal site payment.
- Eligible screen failures receive 50% of the screening payment, subject to the site limit of 20% of randomised subjects.
- A 10% holdback is retained for eligible site payments.
- Holdbacks are released at database lock when the site has no unresolved queries.
Site Payment Amounts and Rules

The site payment amounts are defined as follows:

Payment Type| Amount
Screening payment| ₹12,000
Follow-up visit payment| ₹8,000
End-of-study (EOS) payment| ₹15,000
Screen failure payment| 50% of screening payment

Site Payment Rules:

1. Screening payment is earned on the subject's screening date.
2. Screen failure payments are limited to 20% of the site's randomised subjects.
3. Completed out-of-window visits receive 80% of the applicable site payment.
4. A 10% holdback is applied to site payments.
5. Holdback is released at database lock if there are no unresolved queries.
6. Each unresolved query beyond 15 days results in a ₹500 deduction from the next site payment.
7. If a site has 20 or more open queries, all payments are withheld until the number of open queries falls below 10.
8. TDS of 10% is applied to site payments.
9. Payments must follow the monthly settlement cycle and source-document verification rules.

4.9 Query Management (BR-09)

- Queries must be resolved within 15 days.
- Each query unresolved beyond 15 days incurs a Rs 500 deduction from the next site payment.
- When a site has 20 or more open queries, all site payments are withheld.
- Payment withholding continues until the number of open queries falls below 10.

4.10 Monthly Settlement (BR-10)

- Monthly payment processing considers eligible activities completed during the relevant month.
- Source Data Verification (SDV) must be completed before a visit payment is processed.
- Payments for visits awaiting SDV are carried forward to the month in which verification is completed.
- Site payments are subject to 10% Tax Deducted at Source (TDS).
- Subject payments are tax-free up to Rs 50,000 per subject per financial year. Excess amounts are flagged.
- Database lock releases eligible site holdbacks when there are no unresolved queries.

4.11 Validation and Processing Principles

The engine must validate events before changing trial state.

The following precedence is used when applying business rules:

1. Site status restrictions.
2. Site and trial enrolment caps.
3. Screening eligibility.
4. Consent validity.
5. Randomisation using the correct stratum sequence.
6. Visit scheduling and classification.
7. Deviation tracking.
8. Payment eligibility and settlement.

Rejected commands must be recorded in errors.csv with the corresponding reason code. Rejected commands must not change the trial state.

5. Error Handling and Testing Strategy

5.1 Error Handling

The system must handle invalid commands and business rule violations without crashing or corrupting the trial state.

When a command is rejected:

1. The command must be identified as invalid.
2. The appropriate rejection reason must be determined.
3. The command's line number and name must be recorded.
4. The rejection must be written to errors.csv.
5. The trial state must remain unchanged.

5.2 Important Error Conditions

The system must handle the following rejection conditions:

Error condition| Expected reason code
Site enrolment limit reached| SITE_CAP
Overall trial enrolment limit reached| TRIAL_CAP
Site IRB expired or site on hold| SITE_ON_HOLD
Randomisation outside consent period| CONSENT_EXPIRED
Subject fails screening| SCREEN_FAILED
Re-screen attempted too early| RESCREEN_TOO_EARLY
Re-screen attempted after a non-laboratory failure| Invalid re-screen rejection

The implementation will use the exact reason codes required by the sample pack and project specification.

5.3 Testing Strategy

The project will use automated tests with pytest.

Testing will cover:

1. Protocol loading and validation.
2. Subject inclusion and exclusion criteria.
3. Re-screening conditions.
4. Site and trial enrolment caps.
5. Block randomisation and stratification.
6. Consent validity.
7. Visit date calculations and classifications.
8. Deviation thresholds and PI acknowledgement.
9. Subject withdrawal and Early Termination.
10. Subject and site payment calculations.
11. Query deductions and payment withholding.
12. Monthly settlement and database lock.
13. Invalid commands and error reporting.

5.4 Edge Case Testing

The system will test boundary conditions specified in the sample data pack, including:

- Subject age exactly 65.
- Randomisation exactly 14 days after consent.
- Trial cap reached during same-day randomisations.
- Visit completed on the last allowed window date.
- Missed visit at exactly seven days after window closure.
- Incomplete final randomisation block.
- Travel distance exactly 80 km.
- Site major deviation rate exactly 10%.
- Site IRB expiry and renewal.
- Re-screening after laboratory failure.
- Multiple unresolved queries.

5.5 Test Execution

Automated tests will be stored in the tests directory.

Tests will be executed using:

python -m pytest

The sample data pack will be used for integration testing. Additional tests will verify individual business rules and boundary conditions.

5.6 Expected Quality

The testing process aims to ensure:

- Correct business rule implementation.
- Accurate calculations.
- Consistent trial state.
- Correct rejection of invalid commands.
- Reliable generation of all six output CSV files.

6. Execution Flow, Assumptions and Limitations

6.1 Execution Flow

The application follows these execution steps:

1. Start the Python application using main.py.
2. Load the protocol arms and visit schedules.
3. Load laboratory ranges and exclusion conditions.
4. Load site information and randomisation block sequences.
5. Load subject screening records.
6. Read commands from commands.txt.
7. Process each command sequentially.
8. Validate the command against the relevant business rules.
9. Update the application state when the command is accepted.
10. Record rejected commands in errors.csv without changing the trial state.
11. Process MONTH_END and DB_LOCK commands when encountered.
12. Generate the required output CSV reports.

6.2 Project Assumptions

The implementation follows the conventions documented in the sample data pack:

- Dates use YYYY-MM-DD format.
- Timestamps use YYYY-MM-DD HH:MM:SS format in Indian Standard Time.
- Subject numbers follow the format SITE-NNN.
- Subject age is calculated in completed years on the consent date.
- Age bands are based on age below 45 and age 45 or above.
- The four randomisation strata are M_LT45, M_GE45, F_LT45 and F_GE45.
- Randomisation uses the supplied block sequences.
- Events are processed in command-file order.
- Events occurring on the same day follow their order in commands.txt.
- Empty CSV cells represent non-applicable values where permitted by the data specification.
- Money values are represented as decimal amounts without currency symbols or commas.

6.3 Project Limitations

- The application is command-file driven and does not include a graphical user interface.
- The system processes the supplied sample data and command files.
- The project does not connect to external hospital or clinical trial management systems.
- The application generates CSV reports rather than interactive dashboards.
- The system follows the business rules and conventions supplied in the project specification and sample data pack.

6.4 Expected Deliverables

The final project submission will include:

1. Python source code.
2. Input sample data files.
3. Automated test suite.
4. Project README.
5. Design document in PDF format.
6. Decision log.
7. Five-minute project demonstration video link.
8. Required output CSV reports.

6.5 Conclusion

The Clinical Trial Site Enrolment, Visit Window and Subject Payment Engine provides a structured approach to managing clinical trial operations.

By implementing protocol validation, subject screening, block randomisation, visit tracking, deviation management and payment processing, the system aims to ensure consistent application of clinical trial business rules.

The modular Python architecture supports testing, maintenance and future improvements.