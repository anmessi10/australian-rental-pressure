from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RENTAL_PATH = PROJECT_ROOT / "data" / "processed" / "rental_sa2_2021.csv"
POPULATION_PATH = PROJECT_ROOT / "data" / "processed" / "population_sa2_clean.csv"
INCOME_PATH = PROJECT_ROOT / "data" / "processed" / "income_sa2_clean.csv"

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_model_dataset_2021.csv"
)


def main():
    rental = pd.read_csv(
        RENTAL_PATH,
        dtype={"sa2_code": str}
    )

    population = pd.read_csv(
        POPULATION_PATH,
        dtype={"sa2_code": str}
    )

    income = pd.read_csv(
        INCOME_PATH,
        dtype={"sa2_code": str}
    )

    # Standardise SA2 identifiers.
    for df in [rental, population, income]:
        df["sa2_code"] = (
            df["sa2_code"]
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
            .str.zfill(9)
        )

    # Keep 2021 population.
    population_2021 = population[
        population["year"] == 2021
    ][
        ["sa2_code", "state", "sa2", "population"]
    ].copy()

    # Keep 2021 income.
    income_2021 = income[
        income["year"] == 2021
    ][
        ["sa2_code", "median_employee_income"]
    ].copy()

    # Combine the datasets.
    model = (
        rental[
            [
                "sa2_code",
                "rented_dwellings",
                "estimated_median_weekly_rent",
            ]
        ]
        .merge(
            population_2021,
            on="sa2_code",
            how="inner",
        )
        .merge(
            income_2021,
            on="sa2_code",
            how="left",
        )
    )

    print("Initial combined dataset:", len(model))

    # Keep observations with a valid rental target,
    # valid income and positive population.
    model = model[
        model["estimated_median_weekly_rent"].notna()
        & model["median_employee_income"].notna()
        & (model["population"] > 0)
    ].copy()

    # Create useful modelling features.
    model["annualised_estimated_rent"] = (
        model["estimated_median_weekly_rent"] * 52
    )

    model["estimated_rent_to_income_pct"] = (
        model["annualised_estimated_rent"]
        / model["median_employee_income"]
        * 100
    )

    # Sort by SA2 code.
    model = model.sort_values("sa2_code")

    # Validate uniqueness.
    duplicate_count = model.duplicated(
        subset=["sa2_code"]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate SA2 records."
        )

    # Save.
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    model.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"Saved: {OUTPUT_PATH}")
    print(f"Final rows: {len(model):,}")
    print(f"Final columns: {len(model.columns)}")
    print(f"Duplicate SA2s: {duplicate_count}")

    print("\nMissing values:")
    print(model.isna().sum().to_string())

    print("\nFinal columns:")
    print(model.columns.tolist())

    print("\nPreview:")
    print(model.head(10).to_string(index=False))


if __name__ == "__main__":
    main()