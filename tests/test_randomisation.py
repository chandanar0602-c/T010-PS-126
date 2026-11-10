import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from loader import load_all_data
from randomisation import RandomisationEngine



def test_block_sequences():

    data = load_all_data()

    engine = RandomisationEngine(data["blocks"])

    print("\nBLOCK SEQUENCE TEST")
    print("===================")

    for stratum in ["M_LT45", "M_GE45", "F_LT45", "F_GE45"]:

        rows = sorted(
            [
                row for row in data["blocks"]
                if row["stratum"] == stratum
            ],
            key=lambda row: (
                int(row["block_no"]),
                int(row["position"])
            )
        )

        print(f"\nStratum: {stratum}")

        for row in rows[:4]:
            print(
                "Block:", row["block_no"],
                "| Position:", row["position"],
                "| Arm:", row["arm_id"]
            )

        assert len(rows) == 80

    print("\nAll four strata contain 20 blocks of 4 positions.")
    print("Block sequence test passed!")


if __name__ == "__main__":
    test_block_sequences()