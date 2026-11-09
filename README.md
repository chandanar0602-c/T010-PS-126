# PS-126 – Clinical Trial Site Enrolment, Visit Window and Subject Payment Engine — Sample Data Pack

Prepared by 10 SECONDS for Team T010.

Input for a clinical-trial enrolment, visit-window and payment engine. One protocol (2 arms, 1:1, 6 follow-up visits), 6 sites, 300 screening records, block sequences for 4 strata and an event file covering 2026-03-01 … 2026-10-31 with 1309 visit / SDV / deviation-acknowledgement / query / withdrawal events plus the SCREEN and RANDOMISE commands, site status events and month ends.

Pack conventions where the brief is silent: subjects are referenced in every command by `screening_id`; your engine assigns the subject number `<site_id>-NNN` (e.g. BLR-001) in randomisation order per site and the arm from the next free position of the stratum's block sequence. Age is completed years on the consent date (also used for the age band). 'Within 90 days' of a prior trial and 'within 14 days' of consent are inclusive. A pending protocol visit becomes MISSED when a command is processed whose date is later than window close + 7 days. The FOR_AUDIT check is done at each MONTH_END over all protocol visits (D7–D168) classified so far at that site; ET visits are not counted. Screening site payment is earned on the SCREEN date; travel is reimbursed for protocol and ET visits only.

## Files

| File | What it holds | Rows |
|---|---|---|
| `protocol_arms.csv` | Treatment arms and allocation ratio | 2 data rows |
| `protocol_visits.csv` | Visit schedule, windows and payment rates | 8 data rows |
| `lab_ranges.csv` | Inclusion lab ranges | 4 data rows |
| `exclusion_conditions.csv` | Exclusion conditions | 6 data rows |
| `sites.csv` | Sites with caps, activation and IRB expiry | 6 data rows |
| `block_sequences.csv` | Block randomisation sequence per stratum (block size 4) | 320 data rows |
| `subjects.csv` | Screening records (one per consent, including re-screens) | 300 data rows |
| `commands.txt` | Load commands, then screening, randomisation, visit, query and site events in time order | 1878 command lines (excluding comments) |

Row numbers quoted below are 1-based data-row numbers (the header is row 0). Line numbers for `commands.txt` are physical line numbers including comment lines.

## Column reference

Conventions: dates `YYYY-MM-DD`; timestamps `YYYY-MM-DD HH:MM:SS` (24h, IST, no timezone suffix); money in Rs as plain decimals with up to 2 places (no commas, no symbol); percentages as plain numbers (12.5 = 12.5%); booleans `true`/`false`; IDs uppercase with a fixed prefix. A cell shown as empty in a CSV means "not applicable" and is only allowed where the notes say so.

### `protocol_arms.csv`

| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| arm_id | string | ARM-x | ARM-A, ARM-B | — |
| arm_name | string | — | — | — |
| allocation_ratio | integer | — | 1 | 1:1 |

### `protocol_visits.csv`

| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| visit_code | string | — | SCREENING, D7, D14, D28, D56, D84, D168, ET | D168 is end of study |
| day_offset | integer | days from Day 0 | — | Day 0 = randomisation date |
| window_minus_days | integer | days | — | — |
| window_plus_days | integer | days | — | ET: must happen within 14 days of WITHDRAW |
| subject_payment | decimal | Rs | — | ET pays the next scheduled visit's amount instead |
| site_payment | decimal | Rs | — | 80% for OUT_OF_WINDOW |
| procedures | string | semicolon list | — | informational |

### `lab_ranges.csv`

| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| lab_code | string | — | HB, ALT, CREAT, PLT | — |
| lab_name | string | — | — | — |
| min_value | decimal | unit column | — | inclusive |
| max_value | decimal | unit column | — | inclusive |
| unit | string | — | — | — |

### `exclusion_conditions.csv`

| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| condition_code | string | — | — | — |
| description | string | — | — | — |

### `sites.csv`

| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| site_id | string | 3 letters | BLR, MYS, HYD, CHN, PUN, KOC | also the subject-number prefix |
| site_name | string | — | — | — |
| city | string | — | — | — |
| enrolment_cap | integer | subjects | — | trial cap is 240 overall |
| activation_date | date | — | — | no screening before this date |
| irb_expiry_date | date | — | — | after this date the site is ON_HOLD until IRB_RENEWAL |
| pi_name | string | — | — | — |

### `block_sequences.csv`

| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| stratum | enum | — | M_LT45, M_GE45, F_LT45, F_GE45 | sex × age band |
| block_no | integer | — | 1–20 | — |
| position | integer | — | 1–4 | — |
| arm_id | string | — | protocol_arms.csv | — |

### `subjects.csv`

| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| screening_id | string | SCR-nnnn | — | numbered in consent order |
| site_id | string | — | sites.csv | — |
| consent_ts | timestamp | — | — | screening consent |
| sex | enum | — | M, F | — |
| date_of_birth | date | — | — | — |
| bmi | decimal | kg/m2, 1 decimal | — | eligible 18.5–35.0 inclusive |
| lab_hb | decimal | g/dL | — | — |
| lab_alt | integer | U/L | — | — |
| lab_creat | decimal | mg/dL | — | — |
| lab_plt | integer | 10^3/uL | — | — |
| conditions | string | semicolon list | NONE or condition codes | only codes in exclusion_conditions.csv exclude |
| last_trial_end_date | date | — | — | empty = never in another trial |
| travel_km_one_way | integer | km | — | Rs 10/km, cap Rs 800 per visit |
| rescreen_of | string | — | subjects.csv | empty = first screening |

## Command file format

`commands.txt` holds one command per line as `COMMAND_NAME|arg1|arg2|...`. Commands must be processed in file order, top to bottom. Lines starting with `#` are comments and blank lines are ignored. Every command used in this pack:

| Command | Arguments (in order) | Meaning |
|---|---|---|
| LOAD_PROTOCOL | arms_file\|visits_file | — |
| LOAD_LAB_RANGES / LOAD_EXCLUSIONS / LOAD_SITES / LOAD_BLOCKS / LOAD_SUBJECTS | file | — |
| SCREEN | screening_id\|timestamp | Run inclusion/exclusion → ELIGIBLE or SCREEN_FAILED (or rejected: site on hold, re-screen rules) |
| RANDOMISE | screening_id\|timestamp | Assign subject number and arm, or reject (CONSENT_EXPIRED, SITE_CAP, TRIAL_CAP, SITE_ON_HOLD, SITE_FOR_AUDIT) |
| VISIT | screening_id\|visit_code\|visit_date\|sdv_flag | Record an actual visit; sdv_flag true = source documents verified |
| SDV | screening_id\|visit_code\|date | Source documents verified later (visit is paid in the cycle of this date) |
| WITHDRAW | screening_id\|date\|reason | Subject withdraws; ET visit due within 14 days |
| PI_ACK | screening_id\|date | PI acknowledgement of the subject's deviations |
| QUERY_OPEN | query_id\|site_id\|screening_id\|date | — |
| QUERY_RESOLVE | query_id\|date | — |
| IRB_RENEWAL | site_id\|new_expiry_date\|date | Lifts ON_HOLD |
| CAPA | site_id\|date | Lifts the FOR_AUDIT randomisation pause |
| MONTH_END | date | Classify missed visits, run deviation/audit checks, compute the month's payments |
| DB_LOCK | date | Database lock: release 10% holdbacks for sites with no unresolved queries |
| PRINT_ENROLMENT_DASHBOARD / PRINT_VISIT_CALENDAR / PRINT_DEVIATION_LOG / PRINT_PAYMENT_STATEMENTS | ALL | Print outputs |

Rejected commands go to errors.csv with the reason code and do not change state. Events dated on the same day are in file order.

## Planted scenarios

Every edge case in the brief, mapped to the exact record(s) where it occurs, followed by extra traps.

- **EC-01 Subject exactly 65 years old at consent**
  - subjects.csv row 187 (SCR-0187, site BLR): date_of_birth 1961-07-22, consent 2026-07-22 — 65th birthday on the consent date, age exactly 65 → eligible (18–65 inclusive) and in the ≥ 45 stratum; randomised at commands.txt line 782.
- **EC-02 Randomisation on day 14 after consent**
  - subjects.csv row 35 (SCR-0035, site KOC): consent 2026-05-05, RANDOMISE at commands.txt line 159 on 2026-05-19 = day 14 → allowed (within 14 days, inclusive).
- **EC-03 Trial cap reached by two sites on the same day (ordered by event timestamp)**
  - SCR-0299 (CHN) at 2026-09-24 10:05:00 and SCR-0297 (BLR) at 2026-09-24 11:40:00 are randomisations no. 239 and 240 on the same day (commands.txt lines 1616 and 1618); the trial cap is reached by the second one; SCR-0298 (MYS) tries at 15:20 the same day (line 1624) → rejected TRIAL_CAP. Order by event timestamp.
- **EC-04 Visit on day 31 for the day-28 visit (window +3 means day 31 is in window)**
  - subjects.csv row 59 (SCR-0059, site HYD): randomised 2026-05-20; D28 VISIT at commands.txt line 397 on day 31 (window +3) → IN_WINDOW.
- **EC-05 Missed visit at exactly window + 7 days**
  - subjects.csv row 102 (SCR-0102, site KOC): randomised 2026-06-19; D56 window closes on day 61, window + 7 = day 68; the VISIT at commands.txt line 1249 is on day 68 → recorded OUT_OF_WINDOW (minor), not MISSED.
- **EC-06 Block of 4 with 3 subjects when the stratum closes**
  - Stratum F_GE45 ends with 63 randomised subjects (15 full blocks + 3 subjects in block 16) when the trial cap closes enrolment — the 4th position of that block is never used. Final counts per stratum: F_GE45 63, F_LT45 61, M_GE45 58, M_LT45 58.
- **EC-07 Travel of exactly 80 km**
  - subjects.csv row 110 (SCR-0110, site KOC): travel_km_one_way 80 → Rs 10 × 80 = Rs 800, exactly the per-visit cap (no reduction); compare the trap below at 95 km.
- **EC-08 Site with exactly 10% major-deviation visits**
  - Site PUN (enrolment_cap 5): by MONTH_END 2026-10-31 (commands.txt line 1874) it has 30 classified protocol visits of which 3 are MISSED (major) = exactly 10% → NOT flagged FOR_AUDIT (rule needs over 10%). At every earlier month end its ratio is below 10%.

Extra traps (not in the brief, but realistic — your validation should catch them):

- **FOR_AUDIT site and CAPA** — subjects.csv row 89 (SCR-0089, site CHN) misses D7 and D14 consecutively → LOST_TO_FOLLOW_UP (PI_ACK at line 609); at MONTH_END 2026-07-31 (line 866) site CHN is over 10% major-deviation visits → FOR_AUDIT. RANDOMISE of SCR-0220 at line 963 is rejected (paused); CAPA at line 1048; the retry at line 1062 (day 10 after consent) succeeds.
- **IRB lapse (ON_HOLD)** — site MYS irb_expiry_date 2026-06-30, IRB_RENEWAL at commands.txt line 567 on 2026-07-10. subjects.csv row 141 (SCR-0141, site MYS) SCREEN on 2026-07-06 (line 534) → rejected SITE_ON_HOLD; SCR-0126 RANDOMISE on 2026-07-03 (line 509) → rejected, retried at line 577 on day 12 → accepted. Follow-up visits at MYS during the hold are still accepted.
- **Consent expired (day 15)** — subjects.csv row 18 (SCR-0018, site HYD): RANDOMISE at commands.txt line 81 is 15 days after consent → CONSENT_EXPIRED; the slot is freed.
- **Site cap** — subjects.csv row 16 (SCR-0016, site PUN): site PUN already has 5 randomised subjects → RANDOMISE at line 43 rejected SITE_CAP.
- **Re-screens** — subjects.csv row 27 (SCR-0027, site BLR) fails on haemoglobin 11.6; subjects.csv row 70 (SCR-0070, site BLR) re-screens it 31 days later (rescreen_of) → allowed and passes. subjects.csv row 43 (SCR-0043, site BLR) fails on ALT 68 and subjects.csv row 74 (SCR-0074, site BLR) re-screens after only 20 days → rejected RESCREEN_TOO_EARLY. subjects.csv row 163 (SCR-0163, site HYD) fails on BMI 35.9; subjects.csv row 266 (SCR-0266, site HYD) re-screen → rejected (failure was not a lab value).
- **Prior trial exactly 90 days** — subjects.csv row 8 (SCR-0008, site HYD): last_trial_end_date is exactly 90 days before consent → excluded (pack convention: 'within 90 days' is inclusive).
- **BMI boundary** — subjects.csv row 121 (SCR-0121, site BLR) BMI 35.0 → eligible; subjects.csv row 9 (SCR-0009, site CHN) BMI 35.1 → SCREEN_FAILED.
- **Age band boundary** — subjects.csv row 147 (SCR-0147, site KOC): exactly 45 at consent → stratum ≥ 45.
- **Travel cap** — subjects.csv row 91 (SCR-0091, site HYD): 95 km one way → Rs 950, capped at Rs 800 per visit.
- **Minor deviations beyond 3** — subjects.csv row 96 (SCR-0096, site BLR) has 4 OUT_OF_WINDOW visits (D7, D14, D28, D56) and no PI_ACK → PI acknowledgement overdue; subjects.csv row 13 (SCR-0013, site HYD) has the same pattern and a PI_ACK at line 425 within 10 days.
- **Withdrawal and early termination** — subjects.csv row 114 (SCR-0114, site HYD): WITHDRAW at line 954; ET VISIT 9 days later at line 1099 → subject paid the amount of the next scheduled visit; the slot is NOT freed.
- **Visit before the previous window opens** — subjects.csv row 81 (SCR-0081, site HYD): VISIT D28 on day 10 at line 389 — the D14 window opens on day 12 → rejected with an error line.
- **Query timelines** — query resolved exactly 15 days after opening (lines 87/161) → no deduction; query resolved after 16 days (lines 94/175) → Rs 500 deduction. Site KOC gets 21 queries opened 2026-08-03…07 (lines 892–990) → 20+ open, payments withheld until fewer than 10 remain open (after the resolutions in late September).
- **Screen-failure payment cap** — site HYD has 27 screen failures against 45 randomised subjects → only 20% of randomised (9) screen failures are paid at 50% of Rs 12,000.

## What is NOT in this pack

Expected outputs are not provided for this set. Validate your engine with your own test suite against the rules in your brief (BR-01 … BR-12). A separate hidden input set with the same schema will be used at final evaluation; outputs are compared field-for-field, so follow the column formats above exactly in your own output.

## Output format expected at evaluation

Produce these files (CSV, UTF-8, header row, same conventions as above). Column order matters. Where the brief is silent on a format detail, the choice below is binding for evaluation.

### `screening_outcomes.csv`

One row per SCREEN command.

Columns in order: `screening_id`, `site_id`, `screen_date`, `outcome`, `failed_criteria`

### `randomisations.csv`

One row per successful RANDOMISE.

Columns in order: `screening_id`, `subject_number`, `site_id`, `randomisation_ts`, `stratum`, `block_no`, `position`, `arm_id`

### `visit_calendar.csv`

One row per protocol visit per randomised subject (scheduled, actual, classification).

Columns in order: `subject_number`, `visit_code`, `target_date`, `window_open`, `window_close`, `actual_date`, `classification`, `deviation`

### `deviation_log.csv`

One row per deviation.

Columns in order: `subject_number`, `visit_code`, `severity`, `detected_date`, `pi_ack_due`, `pi_ack_date`

### `payment_statements.csv`

One row per site per month and per subject per month with any amount.

Columns in order: `month`, `payee_type`, `payee_id`, `gross`, `out_of_window_reduction`, `query_deductions`, `holdback`, `tds`, `withheld`, `net_paid`

### `errors.csv`

Rejected commands.

Columns in order: `line_no`, `command`, `reason`

Binding choices: classification is IN_WINDOW, OUT_OF_WINDOW, MISSED or EARLY_TERMINATION; severity MINOR or MAJOR; payee_type SITE or SUBJECT; subject status values ELIGIBLE, SCREEN_FAILED, RANDOMISED, CONSENT_EXPIRED, WITHDRAWN, LOST_TO_FOLLOW_UP, COMPLETED; month as YYYY-MM; use NONE for an empty date.
# T010-PS-126
Clinical trial site enrolment ,visit window and subject payment engine
