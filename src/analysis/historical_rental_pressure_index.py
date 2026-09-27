from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RENTAL_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_trends_2019_2023.csv"
)

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
    / "historical_rental_pressure_index_2019_2023.csv"
)


def z_score(series):
    return (series - series.mean()) / series.std(ddof=0)


def main():

    print("Loading rental trend data...")
    rental = pd.read_csv(RENTAL_DATA)

    print("Loading population and affordability data...")
    population = pd.read_csv(POPULATION_DATA)

    # ---------------------------------------------------------
    # Select required columns
    # ---------------------------------------------------------

    rental = rental[
        [
            "state",
            "rent_change_pct",
        ]
    ].copy()

    population = population[
        [
            "state",
            "population_change_pct",
            "affordability_change_percentage_points",
        ]
    ].copy()

    # ---------------------------------------------------------
    # Merge
    # ---------------------------------------------------------

    print("\nMerging datasets...")

    df = rental.merge(
        population,
        on="state",
        how="inner",
        validate="one_to_one",
    )

    print(f"States included: {len(df)}")

    # ---------------------------------------------------------
    # Display raw components
    # ---------------------------------------------------------

    print("\nRaw components:")

    print(
        df[
            [
                "state",
                "rent_change_pct",
                "population_change_pct",
                "affordability_change_percentage_points",
            ]
        ]
        .round(2)
        .to_string(index=False)
    )

    # ---------------------------------------------------------
    # Standardise components
    # ---------------------------------------------------------

    df["rent_growth_z"] = z_score(
        df["rent_change_pct"]
    )

    df["population_growth_z"] = z_score(
        df["population_change_pct"]
    )

    df["affordability_change_z"] = z_score(
        df["affordability_change_percentage_points"]
    )

    # ---------------------------------------------------------
    # Equal-weight composite
    # ---------------------------------------------------------

    df["historical_pressure_z"] = (
        df["rent_growth_z"]
        + df["population_growth_z"]
        + df["affordability_change_z"]
    ) / 3

    # ---------------------------------------------------------
    # Rescale to 0–100
    # ---------------------------------------------------------

    index_min = df["historical_pressure_z"].min()
    index_max = df["historical_pressure_z"].max()

    df["historical_rental_pressure_index"] = (
        (
            df["historical_pressure_z"] - index_min
        )
        / (index_max - index_min)
    ) * 100

    # ---------------------------------------------------------
    # Sort
    # ---------------------------------------------------------

    df = df.sort_values(
        "historical_rental_pressure_index",
        ascending=False,
    )

    # ---------------------------------------------------------
    # Display results
    # ---------------------------------------------------------

    print("\nHistorical Rental Pressure Index:")

    print(
        df[
            [
                "state",
                "rent_change_pct",
                "population_change_pct",
                "affordability_change_percentage_points",
                "historical_rental_pressure_index",
            ]
        ]
        .round(2)
        .to_string(index=False)
    )

    # ---------------------------------------------------------
    # Save
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
        f"\nSaved Historical Rental Pressure Index to:\n"
        f"{OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()