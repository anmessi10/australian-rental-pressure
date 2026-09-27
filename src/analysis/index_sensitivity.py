from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "historical_rental_pressure_index_2019_2023.csv"
)

OUTPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_pressure_index_sensitivity.csv"
)


def z_score(series):
    return (series - series.mean()) / series.std(ddof=0)


def rescale_to_100(series):
    minimum = series.min()
    maximum = series.max()

    return (
        (series - minimum)
        / (maximum - minimum)
    ) * 100


def main():

    print("Loading historical Rental Pressure Index data...")

    df = pd.read_csv(INPUT_DATA)

    # ---------------------------------------------------------
    # Standardise the three underlying components
    # ---------------------------------------------------------

    df["rent_z"] = z_score(
        df["rent_change_pct"]
    )

    df["population_z"] = z_score(
        df["population_change_pct"]
    )

    df["affordability_z"] = z_score(
        df["affordability_change_percentage_points"]
    )

    # ---------------------------------------------------------
    # Weighting scenarios
    # ---------------------------------------------------------

    scenarios = {
        "Equal": {
            "rent": 1 / 3,
            "population": 1 / 3,
            "affordability": 1 / 3,
        },
        "Rental-focused": {
            "rent": 0.50,
            "population": 0.25,
            "affordability": 0.25,
        },
        "Population-focused": {
            "rent": 0.25,
            "population": 0.50,
            "affordability": 0.25,
        },
        "Affordability-focused": {
            "rent": 0.25,
            "population": 0.25,
            "affordability": 0.50,
        },
    }

    results = df[["state"]].copy()

    # ---------------------------------------------------------
    # Calculate each scenario
    # ---------------------------------------------------------

    for scenario_name, weights in scenarios.items():

        composite = (
            df["rent_z"] * weights["rent"]
            + df["population_z"] * weights["population"]
            + df["affordability_z"] * weights["affordability"]
        )

        results[scenario_name] = rescale_to_100(
            composite
        )

    # ---------------------------------------------------------
    # Rankings
    # ---------------------------------------------------------

    ranking = results.copy()

    for column in scenarios:

        ranking[column + " rank"] = (
            ranking[column]
            .rank(
                ascending=False,
                method="min",
            )
            .astype(int)
        )

    # ---------------------------------------------------------
    # Display scores
    # ---------------------------------------------------------

    print("\nSensitivity scores:")

    print(
        results
        .sort_values(
            "Equal",
            ascending=False,
        )
        .round(2)
        .to_string(index=False)
    )

    # ---------------------------------------------------------
    # Display rankings
    # ---------------------------------------------------------

    print("\nSensitivity rankings:")

    ranking_display = ranking[
        [
            "state",
            "Equal rank",
            "Rental-focused rank",
            "Population-focused rank",
            "Affordability-focused rank",
        ]
    ].sort_values("Equal rank")

    print(
        ranking_display
        .to_string(index=False)
    )

    # ---------------------------------------------------------
    # Rank range
    # ---------------------------------------------------------

    rank_columns = [
        column + " rank"
        for column in scenarios
    ]

    ranking["best_rank"] = ranking[rank_columns].min(axis=1)
    ranking["worst_rank"] = ranking[rank_columns].max(axis=1)
    ranking["rank_range"] = (
        ranking["worst_rank"]
        - ranking["best_rank"]
    )

    print("\nRank stability:")

    print(
        ranking[
            [
                "state",
                "best_rank",
                "worst_rank",
                "rank_range",
            ]
        ]
        .sort_values("best_rank")
        .to_string(index=False)
    )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    OUTPUT_DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results.to_csv(
        OUTPUT_DATA,
        index=False,
    )

    print(
        f"\nSaved sensitivity analysis to:\n"
        f"{OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()