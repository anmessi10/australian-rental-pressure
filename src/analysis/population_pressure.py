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
    / "population_pressure_2019_2023.csv"
)


def load_data():
    return pd.read_csv(INPUT_DATA)


def calculate_population_change(df):
    """
    Calculate population growth between 2019 and 2023
    and compare it with the change in the rental
    affordability measure.
    """

    start = (
        df[df["year"] == 2019]
        [
            [
                "state",
                "population",
                "rent_to_median_employee_income_pct",
            ]
        ]
        .rename(
            columns={
                "population": "population_2019",
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
                "population",
                "rent_to_median_employee_income_pct",
            ]
        ]
        .rename(
            columns={
                "population": "population_2023",
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

    result["population_change"] = (
        result["population_2023"]
        - result["population_2019"]
    )

    result["population_change_pct"] = (
        result["population_change"]
        / result["population_2019"]
        * 100
    )

    result["affordability_change_percentage_points"] = (
        result["affordability_ratio_2023"]
        - result["affordability_ratio_2019"]
    )

    return result.sort_values(
        "population_change_pct",
        ascending=False,
    ).reset_index(drop=True)


def calculate_correlation(df):
    """
    Calculate the Pearson correlation between population
    growth and change in the affordability measure.

    This describes an association across the eight
    states/territories and does not establish causation.
    """

    correlation = df[
        [
            "population_change_pct",
            "affordability_change_percentage_points",
        ]
    ].corr().iloc[0, 1]

    return correlation


def validate_data(df):
    print("\nValidation:")

    print(f"States: {len(df)}")

    print(
        f"Duplicate states: "
        f"{df['state'].duplicated().sum()}"
    )

    print("\nMissing values:")

    print(df.isna().sum())

    print("\nPopulation and affordability change:")

    print(
        df.to_string(index=False)
    )

    correlation = calculate_correlation(df)

    print(
        "\nPearson correlation between "
        "population growth and affordability "
        f"change: {correlation:.4f}"
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

    print("Calculating population changes...")

    result = calculate_population_change(df)

    validate_data(result)

    print("\nSaving results...")

    save_data(result)

    print(
        f"Saved to: {OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()