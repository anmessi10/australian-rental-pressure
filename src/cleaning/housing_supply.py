from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

POPULATION_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "population_sa2_clean.csv"
)

BUILDING_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "building_approvals_sa2_clean.csv"
)

OUTPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "housing_supply_sa2_2025_26.csv"
)


EXCLUDED_BUILDING_CODES = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "597979799",
]

MIN_POPULATION_FOR_RATE = 1000


def load_population_data():
    """Load the cleaned ABS SA2 population dataset."""

    df = pd.read_csv(
        POPULATION_DATA,
        dtype={"sa2_code": str},
    )

    return df


def load_building_data():
    """Load the cleaned ABS SA2 building approvals dataset."""

    df = pd.read_csv(
        BUILDING_DATA,
        dtype={"sa2_code": str},
    )

    return df


def prepare_population_data(df):
    """Select 2025 SA2 population data."""

    df = df[df["year"] == 2025].copy()

    df = df[
        [
            "sa2_code",
            "state",
            "gccsa",
            "sa2",
            "population",
        ]
    ].copy()

    # Ensure one population record per SA2
    df = df.drop_duplicates(
        subset=["sa2_code"]
    )

    return df


def prepare_building_data(df):
    """Aggregate new residential dwelling approvals over July 2025-June 2026."""

    # Remove special/placeholder building geography codes
    df = df[
        ~df["sa2_code"].isin(EXCLUDED_BUILDING_CODES)
    ].copy()

    # Sum approvals across the 12-month period
    df = (
        df.groupby(
            "sa2_code",
            as_index=False,
        )["new_residential_dwellings"]
        .sum()
    )

    df = df.rename(
        columns={
            "new_residential_dwellings":
                "approved_dwellings_12m"
        }
    )

    return df


def calculate_housing_supply(population, building):
    """Combine population and building approvals and calculate supply rate."""

    df = population.merge(
        building,
        on="sa2_code",
        how="inner",
    )

    # Calculate approvals per 1,000 residents.
    # Rates are only calculated for SA2s with at least
    # 1,000 residents to avoid unstable rates in very
    # small/special-use areas.
    df["approvals_per_1000"] = (
        df["approved_dwellings_12m"]
        / df["population"]
        * 1000
    )

    df.loc[
        df["population"] < MIN_POPULATION_FOR_RATE,
        "approvals_per_1000",
    ] = pd.NA

    # Calculate the number of SA2s represented in the
    # combined dataset.
    df = df.sort_values(
        ["state", "sa2_code"]
    ).reset_index(drop=True)

    return df


def save_processed_data(df):
    """Save the combined housing supply dataset."""

    OUTPUT_DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_DATA,
        index=False,
    )


def main():
    print("Loading population data...")
    population = load_population_data()

    print("Loading building approvals data...")
    building = load_building_data()

    print("\nPreparing population data...")
    population = prepare_population_data(
        population
    )

    print(
        f"2025 population SA2s: "
        f"{len(population)}"
    )

    print("\nPreparing building approvals...")
    building = prepare_building_data(
        building
    )

    print(
        f"Building SA2s: "
        f"{len(building)}"
    )

    print("\nCombining datasets...")
    df = calculate_housing_supply(
        population,
        building,
    )

    print(
        f"Combined SA2s: "
        f"{len(df)}"
    )

    print("\nValidation:")

    print(
        f"Population range: "
        f"{df['population'].min():.0f} "
        f"to "
        f"{df['population'].max():.0f}"
    )

    print(
        f"Total approved dwellings: "
        f"{df['approved_dwellings_12m'].sum():,.0f}"
    )

    print(
        f"SA2s with population >= "
        f"{MIN_POPULATION_FOR_RATE:,}: "
        f"{(df['population'] >= MIN_POPULATION_FOR_RATE).sum()}"
    )

    print(
        f"SA2s with rate calculated: "
        f"{df['approvals_per_1000'].notna().sum()}"
    )

    print(
        f"SA2s with rate excluded: "
        f"{df['approvals_per_1000'].isna().sum()}"
    )

    print(
        f"Duplicate SA2 rows: "
        f"{df.duplicated(subset=['sa2_code']).sum()}"
    )

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nSample:")
    print(
        df.head(10).to_string(
            index=False
        )
    )

    print("\nSaving dataset...")

    save_processed_data(df)

    print(
        f"Saved to: {OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()