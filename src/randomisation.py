from datetime import datetime


class RandomisationEngine:

    def __init__(self, block_sequences):

        self.block_sequences = block_sequences

        # Track the next position for each stratum
        self.stratum_positions = {}

        # Store successful randomisations
        self.randomised_subjects = []

        # Track site enrolment
        self.site_counts = {}

        # Track randomisation numbers
        self.total_randomised = 0

    def determine_stratum(self, subject):

        sex = subject["sex"].strip().upper()

        consent_date = datetime.strptime(
            subject["consent_ts"],
            "%Y-%m-%d %H:%M:%S"
        ).date()

        dob = datetime.strptime(
            subject["date_of_birth"],
            "%Y-%m-%d"
        ).date()

        age = consent_date.year - dob.year

        if (consent_date.month, consent_date.day) < (
            dob.month, dob.day
        ):
            age -= 1

        age_group = "LT45" if age < 45 else "GE45"

        if sex not in ["M", "F"]:
            raise ValueError("INVALID_SEX")

        return f"{sex}_{age_group}"

    def randomise(self, subject, sites, randomisation_ts):

        screening_id = subject["screening_id"]
        site_id = subject["site_id"]

        # Trial cap
        if self.total_randomised >= 240:
            return None, "TRIAL_CAP"

        # Find registered site
        site = next(
            (s for s in sites if s["site_id"] == site_id),
            None
        )

        if site is None:
            return None, "UNKNOWN_SITE"

        # Site cap
        site_count = self.site_counts.get(site_id, 0)
        site_cap = int(site["enrolment_cap"])

        if site_count >= site_cap:
            return None, "SITE_CAP"

        # Determine subject stratum
        stratum = self.determine_stratum(subject)

        # Get next sequence position
        position_index = self.stratum_positions.get(stratum, 0)

        available_blocks = sorted(
            [
                row for row in self.block_sequences
                if row["stratum"] == stratum
            ],
            key=lambda row: (
                int(row["block_no"]),
                int(row["position"])
            )
        )

        if position_index >= len(available_blocks):
            return None, "BLOCK_SEQUENCE_EXHAUSTED"

        selected = available_blocks[position_index]

        # Assign arm
        arm_id = selected["arm_id"]

        # Assign site-specific subject number
        subject_number = f"{site_id}-{site_count + 1:03d}"

        result = {
            "screening_id": screening_id,
            "subject_number": subject_number,
            "site_id": site_id,
            "randomisation_ts": randomisation_ts,
            "stratum": stratum,
            "block_no": int(selected["block_no"]),
            "position": int(selected["position"]),
            "arm_id": arm_id
        }

        # Update state only after successful randomisation
        self.stratum_positions[stratum] = position_index + 1
        self.site_counts[site_id] = site_count + 1
        self.total_randomised += 1
        self.randomised_subjects.append(result)

        return result, None