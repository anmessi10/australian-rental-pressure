from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

AFFORDABILITY_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "state_affordability_2019_2023.csv"
)

POPULATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "population_pressure_2019_2023.csv"
)

SUPPLY_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "housing_supply_state_2025_26.csv"
)

INDEX_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "historical_rental_pressure_index_2019_2023.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "dashboard_state_master.csv"
)


def main():

    print("Loading analysis datasets...")

    affordability = pd.read_csv(
        AFFORDABILITY_PATH
    )

    population = pd.read_csv(
        POPULATION_PATH
    )

    supply = pd.read_csv(
        SUPPLY_PATH
    )

    index = pd.read_csv(
        INDEX_PATH
    )

    # ---------------------------------------------------------
    # 2023 affordability indicators
    # ---------------------------------------------------------

    affordability_2023 = affordability[
        affordability["year"] == 2023
    ].copy()

    affordability_2023 = affordability_2023[
        [
            "state",
            "year",
            "annual_mean_median_weekly_rent",
            "annualised_median_rent",
            "median_employee_income",
            "rent_to_median_employee_income_pct",
        ]
    ].copy()

    affordability_2023 = affordability_2023.rename(
        columns={
            "year": "affordability_year"
        }
    )

    # ---------------------------------------------------------
    # 2019–2023 population change indicators
    # ---------------------------------------------------------

    population_2023 = population[
        [
            "state",
            "population_2023",
            "population_change_pct",
            "affordability_change_percentage_points",
        ]
    ].copy()

    # ---------------------------------------------------------
    # 2025–26 housing approval indicators
    # ---------------------------------------------------------

    supply = supply[
        [
            "state",
            "population",
            "approved_dwellings_12m",
            "sa2_count",
            "approvals_per_1000",
        ]
    ].copy()

    supply = supply.rename(
        columns={
            "population": "supply_population_2025_26",
            "approved_dwellings_12m": "approved_dwellings_2025_26",
            "sa2_count": "sa2_count_2025_26",
            "approvals_per_1000": "approvals_per_1000_2025_26",
        }
    )

    # ---------------------------------------------------------
    # Historical Rental Pressure Index
    # ---------------------------------------------------------

    index = index[
        [
            "state",
            "historical_rental_pressure_index",
        ]
    ].copy()

    # ---------------------------------------------------------
    # Merge datasets
    # ---------------------------------------------------------

    master = affordability_2023.merge(
        population_2023,
        on="state",
        how="inner",
    )

    master = master.merge(
        supply,
        on="state",
        how="inner",
    )

    master = master.merge(
        index,
        on="state",
        how="inner",
    )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    print("\nMASTER DATASET")
    print("-" * 80)

    print(f"Rows: {len(master)}")
    print(f"Columns: {len(master.columns)}")
    print(f"States: {master['state'].nunique()}")

    print("\nMissing values:")
    print(
        master.isna().sum().to_string()
    )

    print("\nDuplicate states:")
    print(
        master["state"].duplicated().sum()
    )

    print("\nColumns:")
    print(
        master.columns.tolist()
    )

    print("\nPreview:")
    print(
        master.to_string(index=False)
    )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    master.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nSaved: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()