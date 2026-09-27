from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

POPULATION_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "population_sa2_clean.csv"
)

INCOME_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "income_sa2_clean.csv"
)


def main():

    print("Loading SA2 population data...")
    population = pd.read_csv(POPULATION_DATA)

    print("Loading SA2 income data...")
    income = pd.read_csv(INCOME_DATA)

    print("\nPopulation columns:")
    print(population.columns.tolist())

    print("\nIncome columns:")
    print(income.columns.tolist())

    print("\nPopulation years:")
    print(
        sorted(
            population["year"].unique()
        )
    )

    print("\nIncome years:")
    print(
        sorted(
            income["year"].unique()
        )
    )

    # ---------------------------------------------------------
    # Check common SA2-year observations
    # ---------------------------------------------------------

    common = population.merge(
        income,
        on=["sa2_code", "year"],
        how="inner",
    )

    print("\nCommon SA2-year observations:")
    print(len(common))

    print(
        f"Unique SA2s: {common['sa2_code'].nunique()}"
    )

    print(
        f"Years: {sorted(common['year'].unique())}"
    )

    print("\nMissing values in common dataset:")

    print(
        common[
            [
                "population",
                "median_employee_income",
            ]
        ]
        .isna()
        .sum()
    )


if __name__ == "__main__":
    main()