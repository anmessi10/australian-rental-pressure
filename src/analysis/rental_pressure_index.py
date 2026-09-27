from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

AFFORDABILITY_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "population_pressure_2019_2023.csv"
)

HOUSING_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "housing_supply_state_2025_26.csv"
)

OUTPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_pressure_index.csv"
)


def z_score(series):
    """Standardise a numeric series using a z-score."""

    return (
        series - series.mean()
    ) / series.std(ddof=0)


def main():

    print("Loading affordability and population data...")

    affordability = pd.read_csv(
        AFFORDABILITY_DATA
    )

    print("Loading housing approval data...")

    housing = pd.read_csv(
        HOUSING_DATA
    )

    # Keep the 2019–2023 change measures.
    affordability = affordability[
        [
            "state",
            "population_change_pct",
            "affordability_change_percentage_points",
        ]
    ].copy()

    # Keep the state-level approval rate.
    housing = housing[
        [
            "state",
            "approvals_per_1000",
        ]
    ].copy()

    print("\nMerging datasets...")

    df = affordability.merge(
        housing,
        on="state",
        how="inner",
        validate="one_to_one",
    )

    print(
        f"States included: {len(df)}"
    )

    print("\nRaw components:")

    print(
        df.to_string(index=False)
    )

    # ---------------------------------------------------------
    # STANDARDISE COMPONENTS
    # ---------------------------------------------------------

    df[
        "affordability_z"
    ] = z_score(
        df[
            "affordability_change_percentage_points"
        ]
    )

    df[
        "population_growth_z"
    ] = z_score(
        df[
            "population_change_pct"
        ]
    )

    # Higher housing approvals represent more potential
    # new supply, so invert the standardised value.
    df[
        "housing_supply_z"
    ] = z_score(
        df[
            "approvals_per_1000"
        ]
    )

    df[
        "housing_supply_pressure_z"
    ] = (
        -df["housing_supply_z"]
    )

    # ---------------------------------------------------------
    # EQUAL-WEIGHT INDEX
    # ---------------------------------------------------------

    df[
        "rental_pressure_index_z"
    ] = (
        df["affordability_z"]
        + df["population_growth_z"]
        + df["housing_supply_pressure_z"]
    ) / 3

    # Rescale to a more intuitive 0–100 index.
    index_min = df[
        "rental_pressure_index_z"
    ].min()

    index_max = df[
        "rental_pressure_index_z"
    ].max()

    df[
        "rental_pressure_index"
    ] = (
        (
            df["rental_pressure_index_z"]
            - index_min
        )
        / (
            index_max
            - index_min
        )
    ) * 100

    # Sort from highest to lowest index.
    df = df.sort_values(
        "rental_pressure_index",
        ascending=False,
    )

    # ---------------------------------------------------------
    # DISPLAY RESULTS
    # ---------------------------------------------------------

    print(
        "\nRental Pressure Index:"
    )

    print(
        df[
            [
                "state",
                "affordability_change_percentage_points",
                "population_change_pct",
                "approvals_per_1000",
                "rental_pressure_index",
            ]
        ]
        .round(2)
        .to_string(index=False)
    )

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    OUTPUT_DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_DATA,
        index=False,
    )

    print(
        f"\nSaved Rental Pressure Index to:"
        f"\n{OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()