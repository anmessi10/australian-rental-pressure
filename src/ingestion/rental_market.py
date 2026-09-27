from pathlib import Path
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA = PROJECT_ROOT / "data" / "raw" / "Median weekly rent.csv"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed" / "rental_market_clean.csv"


def load_rental_market_data():
    """Load the raw ABS median weekly rent dataset."""

    df = pd.read_csv(RAW_DATA, header=1)

    return df


def clean_rental_market_data(df):
    """Clean and reshape the ABS rental market dataset."""

    # Rename the first column to date
    df = df.rename(columns={"Unnamed: 0": "date"})

    # Convert date values to proper dates
    df["date"] = pd.to_datetime(df["date"], format="%b-%y", errors="coerce")
    df = df.dropna(subset=["date"])

    # Remove currency notation from state column names
    df = df.rename(
        columns={
            "NSW ($)": "NSW",
            "VIC ($)": "VIC",
            "Qld ($)": "QLD",
            "SA ($)": "SA",
            "WA ($)": "WA",
            "TAS ($)": "TAS",
            "NT ($)": "NT",
            "ACT ($)": "ACT",
        }
    )

    # Convert the dataset from wide format to long format
    df = df.melt(
        id_vars="date",
        var_name="state",
        value_name="median_weekly_rent",
    )

    # Ensure rent values are numeric
    df["median_weekly_rent"] = pd.to_numeric(
        df["median_weekly_rent"],
        errors="coerce",
    )

    # Sort the data
    df = df.sort_values(["date", "state"]).reset_index(drop=True)

    return df


def save_processed_data(df):
    """Save the cleaned dataset."""

    PROCESSED_DATA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA, index=False)


def main():
    """Run the rental market ingestion pipeline."""

    print("Loading raw ABS rental market data...")

    df = load_rental_market_data()

    print(f"Raw shape: {df.shape}")

    df = clean_rental_market_data(df)

    print(f"Cleaned shape: {df.shape}")

    print("\nCleaned columns:")
    print(df.columns.tolist())

    print("\nFirst five rows:")
    print(df.head())

    print("\nSaving processed dataset...")

    save_processed_data(df)

    print(f"Saved to: {PROCESSED_DATA}")


if __name__ == "__main__":
    main()