from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DIAGNOSTICS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "model_prediction_diagnostics_2021.csv"
)

POPULATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "population_sa2_clean.csv"
)


def main():

    diagnostics = pd.read_csv(DIAGNOSTICS_PATH)
    population = pd.read_csv(POPULATION_PATH)

    # Standardise SA2 codes
    diagnostics["sa2_code"] = (
        diagnostics["sa2_code"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(9)
    )

    population["sa2_code"] = (
        population["sa2_code"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(9)
    )

    # Get 2021 SA2 information
    pop_2021 = population[
        population["year"] == 2021
    ][
        ["sa2_code", "state", "sa2", "population"]
    ].copy()

    # Remove duplicate SA2 records if any
    pop_2021 = pop_2021.drop_duplicates(
        subset="sa2_code"
    )

    merged = diagnostics.merge(
        pop_2021,
        on="sa2_code",
        how="left",
        suffixes=("", "_population")
    )

    # Show largest errors
    largest_errors = merged.sort_values(
        "absolute_error",
        ascending=False
    ).head(20)

    print("\nLARGEST PREDICTION ERRORS")
    print("=" * 110)

    print(
        largest_errors[
            [
                "sa2_code",
                "sa2",
                "state",
                "population",
                "actual_rent",
                "predicted_rent",
                "residual",
                "absolute_error",
            ]
        ].to_string(index=False)
    )

    # Error summary by state
    state_summary = (
        merged
        .groupby("state")
        .agg(
            observations=("absolute_error", "count"),
            mean_absolute_error=("absolute_error", "mean"),
            median_absolute_error=("absolute_error", "median"),
            max_absolute_error=("absolute_error", "max"),
        )
        .reset_index()
        .sort_values(
            "mean_absolute_error",
            ascending=False
        )
    )

    print("\n\nERROR SUMMARY BY STATE")
    print("=" * 80)

    print(
        state_summary.to_string(index=False)
    )

    # Population of largest-error observations
    print("\n\nPOPULATION DISTRIBUTION OF TOP 20 ERRORS")
    print("=" * 80)

    print(
        largest_errors["population"]
        .describe()
        .to_string()
    )


if __name__ == "__main__":
    main()