from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RENTAL_PATH = PROJECT_ROOT / "data" / "processed" / "rental_sa2_2021.csv"
POPULATION_PATH = PROJECT_ROOT / "data" / "processed" / "population_sa2_clean.csv"
INCOME_PATH = PROJECT_ROOT / "data" / "processed" / "income_sa2_clean.csv"


def main():
    rental = pd.read_csv(RENTAL_PATH, dtype={"sa2_code": str})
    population = pd.read_csv(POPULATION_PATH, dtype={"sa2_code": str})
    income = pd.read_csv(INCOME_PATH, dtype={"sa2_code": str})

    # Standardise SA2 codes.
    for df in [rental, population, income]:
        df["sa2_code"] = (
            df["sa2_code"]
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.zfill(9)
        )

    population_2021 = population[
        population["year"] == 2021
    ].copy()

    income_2021 = income[
        income["year"] == 2021
    ].copy()

    print("\nDATASET SIZES")
    print("-" * 50)
    print(f"Rental 2021:     {len(rental):,} rows")
    print(f"Population 2021: {len(population_2021):,} rows")
    print(f"Income 2021:     {len(income_2021):,} rows")

    print("\nUNIQUE SA2 COUNTS")
    print("-" * 50)
    print(f"Rental:          {rental['sa2_code'].nunique():,}")
    print(f"Population:      {population_2021['sa2_code'].nunique():,}")
    print(f"Income:          {income_2021['sa2_code'].nunique():,}")

    rental_codes = set(rental["sa2_code"])
    population_codes = set(population_2021["sa2_code"])
    income_codes = set(income_2021["sa2_code"])

    common_all = (
        rental_codes
        & population_codes
        & income_codes
    )

    print("\nSA2 OVERLAP")
    print("-" * 50)
    print(f"Rental + Population:              {len(rental_codes & population_codes):,}")
    print(f"Rental + Income:                  {len(rental_codes & income_codes):,}")
    print(f"Population + Income:              {len(population_codes & income_codes):,}")
    print(f"Rental + Population + Income:     {len(common_all):,}")

    # Build the candidate modelling dataset.
    model = (
        rental[
            [
                "sa2_code",
                "rented_dwellings",
                "estimated_median_weekly_rent",
            ]
        ]
        .merge(
            population_2021[
                ["sa2_code", "state", "sa2", "population"]
            ],
            on="sa2_code",
            how="inner",
        )
        .merge(
            income_2021[
                ["sa2_code", "median_employee_income"]
            ],
            on="sa2_code",
            how="left",
        )
    )

    print("\nCANDIDATE MODEL DATASET")
    print("-" * 50)
    print(f"Rows: {len(model):,}")
    print(f"Unique SA2s: {model['sa2_code'].nunique():,}")

    print("\nMISSING VALUES")
    print("-" * 50)
    print(model.isna().sum().to_string())

    print("\nRENT TARGET SUMMARY")
    print("-" * 50)
    print(
        model["estimated_median_weekly_rent"]
        .describe()
        .to_string()
    )

    print("\nINCOME SUMMARY")
    print("-" * 50)
    print(
        model["median_employee_income"]
        .describe()
        .to_string()
    )

    print("\nPOPULATION SUMMARY")
    print("-" * 50)
    print(
        model["population"]
        .describe()
        .to_string()
    )


if __name__ == "__main__":
    main()