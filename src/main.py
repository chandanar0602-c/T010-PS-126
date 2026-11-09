from loader import load_all_data, load_commands
from validation import validate_data


def main():

    print("CLINICAL TRIAL ENGINE")
    print("=====================")

    data = load_all_data()
    commands = load_commands()

    print("\nDATA LOADING SUCCESSFUL")

    for name, records in data.items():
        print(f"{name}: {len(records)} records")

    print("\nVALIDATION")
    print("----------")

    errors = validate_data(data)

    if errors:
        print("Validation failed:")

        for error in errors:
            print("-", error)

    else:
        print("Protocol and site validation successful!")

    print("\nTotal commands:", len(commands))


if __name__ == "__main__":
    main()