from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "state_affordability_2019_2023.csv"
)

OUTPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_trends_2019_2023.csv"
)


def load_data():
    return pd.read_csv(INPUT_DATA)


def calculate_rental_change(df):
    """
    Calculate the change in annual mean median weekly rent
    between 2019 and 2023 for each state.
    """

    start = (
        df[df["year"] == 2019]
        [
            [
                "state",
                "annual_mean_median_weekly_rent",
            ]
        ]
        .rename(
            columns={
                "annual_mean_median_weekly_rent":
                    "rent_2019"
            }
        )
    )

    end = (
        df[df["year"] == 2023]
        [
            [
                "state",
                "annual_mean_median_weekly_rent",
            ]
        ]
        .rename(
            columns={
                "annual_mean_median_weekly_rent":
                    "rent_2023"
            }
        )
    )

    result = start.merge(
        end,
        on="state",
        how="inner",
    )

    result["rent_change_dollars"] = (
        result["rent_2023"]
        - result["rent_2019"]
    )

    result["rent_change_pct"] = (
        result["rent_change_dollars"]
        / result["rent_2019"]
        * 100
    )

    result = result.sort_values(
        "rent_change_pct",
        ascending=False,
    ).reset_index(drop=True)

    return result


def validate_data(df):
    print("\nValidation:")

    print(f"States: {len(df)}")

    print(
        f"Duplicate states: "
        f"{df['state'].duplicated().sum()}"
    )

    print("\nMissing values:")

    print(df.isna().sum())

    print("\nRental change 2019-2023:")

    print(
        df.to_string(index=False)
    )


def save_data(df):
    OUTPUT_DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_DATA,
        index=False,
    )


def main():

    print("Loading affordability dataset...")

    df = load_data()

    print("Calculating rental changes...")

    result = calculate_rental_change(df)

    validate_data(result)

    print("\nSaving results...")

    save_data(result)

    print(
        f"Saved to: {OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()