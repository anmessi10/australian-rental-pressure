from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "building_approvals"
    / "sa2_2526_formatted.csv"
)

PROCESSED_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "building_approvals_sa2_clean.csv"
)


def load_building_approvals():
    """Load the ABS SA2 building approvals dataset."""
    df = pd.read_csv(
        RAW_DATA,
        low_memory=False,
    )
    return df


def clean_building_approvals(df):
    """Filter and clean new residential dwelling approvals."""

    # Keep new residential construction for all ownership sectors
    df = df[
        (df["type_work"] == 1)
        & (df["type_bld"] == 100)
        & (df["own_sector"] == 9)
    ].copy()

    # Convert numeric fields before filtering
    df["dwl"] = pd.to_numeric(
        df["dwl"],
        errors="coerce",
    )

    df["val"] = pd.to_numeric(
        df["val"],
        errors="coerce",
    )

    # Remove aggregate Australia row
    df = df[df["sa2_code"] != 0].copy()

    # Remove special/placeholder regions with no approved dwellings
    df = df[df["dwl"] > 0].copy()

    # Keep only the fields needed for analysis
    df = df[
        [
            "app_month",
            "sa2_code",
            "dwl",
            "val",
        ]
    ].copy()

    # Rename columns
    df = df.rename(
        columns={
            "app_month": "date",
            "dwl": "new_residential_dwellings",
            "val": "building_value_thousand",
        }
    )

    # Convert date
    df["date"] = pd.to_datetime(
        df["date"],
        format="%Y-%m",
        errors="coerce",
    )

    # Convert SA2 code
    df["sa2_code"] = pd.to_numeric(
        df["sa2_code"],
        errors="coerce",
    )

    # Convert numeric fields again after column selection/renaming
    df["new_residential_dwellings"] = pd.to_numeric(
        df["new_residential_dwellings"],
        errors="coerce",
    )

    df["building_value_thousand"] = pd.to_numeric(
        df["building_value_thousand"],
        errors="coerce",
    )

    # Remove invalid records
    df = df.dropna(
        subset=[
            "date",
            "sa2_code",
            "new_residential_dwellings",
        ]
    )

    # SA2 codes are identifiers, not measurements
    df["sa2_code"] = (
        df["sa2_code"]
        .astype("Int64")
        .astype(str)
    )

    # Sort
    df = df.sort_values(
        ["sa2_code", "date"]
    ).reset_index(drop=True)

    return df


def save_processed_data(df):
    """Save the cleaned dataset."""

    PROCESSED_DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        PROCESSED_DATA,
        index=False,
    )


def main():
    print("Loading ABS building approvals data...")

    df = load_building_approvals()

    print(f"Raw shape: {df.shape}")

    df = clean_building_approvals(df)

    print(f"Cleaned shape: {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nDate range:")
    print(
        f"{df['date'].min().date()} "
        f"to "
        f"{df['date'].max().date()}"
    )

    print("\nNumber of SA2 regions:")
    print(df["sa2_code"].nunique())

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicate SA2-month rows:")
    print(
        df.duplicated(
            subset=["sa2_code", "date"]
        ).sum()
    )

    print("\nTotal new residential dwellings:")
    print(
        df["new_residential_dwellings"].sum()
    )

    print("\nSaving processed dataset...")

    save_processed_data(df)

    print(f"Saved to: {PROCESSED_DATA}")


if __name__ == "__main__":
    main()