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
    / "affordability_trends_2019_2023.csv"
)


def load_data():
    return pd.read_csv(INPUT_DATA)


def calculate_affordability_change(df):
    """
    Calculate the change in the project-created
    rent-to-median-employee-income measure between
    2019 and 2023.
    """

    start = (
        df[df["year"] == 2019]
        [
            [
                "state",
                "median_employee_income",
                "rent_to_median_employee_income_pct",
            ]
        ]
        .rename(
            columns={
                "median_employee_income":
                    "income_2019",
                "rent_to_median_employee_income_pct":
                    "affordability_ratio_2019",
            }
        )
    )

    end = (
        df[df["year"] == 2023]
        [
            [
                "state",
                "median_employee_income",
                "rent_to_median_employee_income_pct",
            ]
        ]
        .rename(
            columns={
                "median_employee_income":
                    "income_2023",
                "rent_to_median_employee_income_pct":
                    "affordability_ratio_2023",
            }
        )
    )

    result = start.merge(
        end,
        on="state",
        how="inner",
    )

    result["income_change_dollars"] = (
        result["income_2023"]
        - result["income_2019"]
    )

    result["income_change_pct"] = (
        result["income_change_dollars"]
        / result["income_2019"]
        * 100
    )

    result["affordability_ratio_change_percentage_points"] = (
        result["affordability_ratio_2023"]
        - result["affordability_ratio_2019"]
    )

    result = result.sort_values(
        "affordability_ratio_change_percentage_points",
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

    print("\nAffordability change 2019-2023:")

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

    print("Loading state affordability dataset...")

    df = load_data()

    print("Calculating affordability changes...")

    result = calculate_affordability_change(df)

    validate_data(result)

    print("\nSaving results...")

    save_data(result)

    print(
        f"Saved to: {OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()