import csv
from pathlib import Path


# Project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data folder
DATA_DIR = PROJECT_ROOT / "data"


def load_csv(filename):
    """
    Read a CSV file and return its records as a list of dictionaries.
    """

    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file not found: {file_path}"
        )

    with open(file_path, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return list(reader)


def load_commands(filename="commands.txt"):
    """
    Read commands from commands.txt.
    Ignore blank lines and comment lines.
    """

    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required command file not found: {file_path}"
        )

    commands = []

    with open(file_path, mode="r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = [part.strip() for part in line.split("|")]

            commands.append({
                "line_no": line_number,
                "command": parts[0],
                "arguments": parts[1:]
            })

    return commands
def load_all_data():
    """
    Load all input CSV files required by the project.
    """

    data = {
        "arms": load_csv("protocol_arms.csv"),
        "visits": load_csv("protocol_visits.csv"),
        "lab_ranges": load_csv("lab_ranges.csv"),
        "exclusions": load_csv("exclusion_conditions.csv"),
        "sites": load_csv("sites.csv"),
        "blocks": load_csv("block_sequences.csv"),
        "subjects": load_csv("subjects.csv")
    }

    return data