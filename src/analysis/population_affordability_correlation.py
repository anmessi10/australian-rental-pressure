from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

POPULATION_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "population_pressure_2019_2023.csv"
)

OUTPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "population_affordability_correlation.csv"
)


def main():

    print("Loading population-pressure data...")

    df = pd.read_csv(POPULATION_DATA)

    print(
        f"States/territories: {len(df)}"
    )

    print("\nColumns:")
    print(df.columns.tolist())

    # Calculate Pearson correlation between:
    # population growth from 2019 to 2023
    # and change in the affordability ratio
    correlation = df[
        [
            "population_change_pct",
            "affordability_change_percentage_points",
        ]
    ].corr(
        method="pearson"
    ).loc[
        "population_change_pct",
        "affordability_change_percentage_points",
    ]

    print("\nPearson correlation:")

    print(
        f"Population growth vs "
        f"affordability change: {correlation:.4f}"
    )

    print("\nState-level data:")

    print(
        df[
            [
                "state",
                "population_change_pct",
                "affordability_change_percentage_points",
            ]
        ]
        .sort_values(
            "population_change_pct",
            ascending=False,
        )
        .to_string(index=False)
    )

    # Save correlation result.
    result = pd.DataFrame(
        {
            "analysis": [
                "Population growth vs affordability change"
            ],
            "pearson_correlation": [
                correlation
            ],
            "observations": [
                len(df)
            ],
        }
    )

    OUTPUT_DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        OUTPUT_DATA,
        index=False,
    )

    print(
        f"\nSaved correlation result to: "
        f"{OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()