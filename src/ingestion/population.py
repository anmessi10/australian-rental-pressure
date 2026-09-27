from pathlib import Path
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA = PROJECT_ROOT / "data" / "raw" / "32180DS0003_2001-25.xlsx"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed" / "population_sa2_clean.csv"


def load_population_data():
    """Load the ABS SA2 population data."""

    df = pd.read_excel(
        RAW_DATA,
        sheet_name="Table 1",
        header=5,
    )
    year_columns = list(range(2001, 2026))
    df.columns = (
        [
            "S/T code",
            "S/T name",
            "GCCSA code",
            "GCCSA name",
            "SA4 code",
            "SA4 name",
            "SA3 code",
            "SA3 name",
            "SA2 code",
            "SA2 name",
        ]
        + year_columns
    )
    return df


def clean_population_data(df):
    """Clean and reshape the ABS SA2 population dataset."""

    # Rename geography columns
    df = df.rename(
        columns={
            "S/T code": "state_code",
            "S/T name": "state",
            "GCCSA code": "gccsa_code",
            "GCCSA name": "gccsa",
            "SA4 code": "sa4_code",
            "SA4 name": "sa4",
            "SA3 code": "sa3_code",
            "SA3 name": "sa3",
            "SA2 code": "sa2_code",
            "SA2 name": "sa2",
        }
    )

    # Keep only the geography columns and population years
    geography_columns = [
        "state_code",
        "state",
        "gccsa_code",
        "gccsa",
        "sa4_code",
        "sa4",
        "sa3_code",
        "sa3",
        "sa2_code",
        "sa2",
    ]

    population_columns = list(range(2001, 2026))

    df = df[geography_columns + population_columns]

    # Convert population data from wide format to long format
    df = df.melt(
        id_vars=geography_columns,
        var_name="year",
        value_name="population",
    )

    # Convert data types
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["population"] = pd.to_numeric(
        df["population"],
        errors="coerce",
    )

    # Remove rows without a valid SA2 or population value
    df = df.dropna(subset=["sa2_code", "sa2", "population"])

    # Make codes strings so leading zeros are preserved where applicable
    df["state_code"] = df["state_code"].astype("Int64").astype(str) 
    df["gccsa_code"] = df["gccsa_code"].astype(str)
    df["sa4_code"] = df["sa4_code"].astype("Int64").astype(str)
    df["sa3_code"] = df["sa3_code"].astype("Int64").astype(str)
    df["sa2_code"] = df["sa2_code"].astype("Int64").astype(str)

    # Sort the data
    df = df.sort_values(
        ["sa2_code", "year"]
    ).reset_index(drop=True)

    return df


def save_processed_data(df):
    """Save the cleaned population dataset."""

    PROCESSED_DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        PROCESSED_DATA,
        index=False,
    )


def main():
    """Run the population ingestion pipeline."""

    print("Loading ABS SA2 population data...")

    df = load_population_data()

    print(f"Raw shape: {df.shape}")

    df = clean_population_data(df)

    print(f"Cleaned shape: {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst five rows:")
    print(df.head())

    print("\nYear range:")
    print(
        f"{int(df['year'].min())} to "
        f"{int(df['year'].max())}"
    )

    print("\nNumber of SA2 regions:")
    print(df["sa2_code"].nunique())

    print("\nSaving processed dataset...")

    save_processed_data(df)

    print(f"Saved to: {PROCESSED_DATA}")


if __name__ == "__main__":
    main()