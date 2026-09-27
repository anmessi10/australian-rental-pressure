from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA = (
    PROJECT_ROOT / "data" / "raw" / "14100DO0004_2011-25.xlsx"
)

OUTPUT_DATA = (
    PROJECT_ROOT / "data" / "processed" / "income_sa2_clean.csv"
)

START_YEAR = 2019
END_YEAR = 2023


def load_income_data():
    """Load the ABS Data by Region income workbook."""
    return pd.read_excel(
        RAW_DATA,
        sheet_name="Table 1",
        header=6,
        dtype={"Code": str},
    )


def prepare_income_data(df):
    """Keep SA2 records and the 2019-2023 income period."""

    df = df[df["Code"].str.len() == 9].copy()

    df = df[df["Year"].between(START_YEAR, END_YEAR)].copy()

    df = df[
        [
            "Code",
            "Label",
            "Year",
            "Median employee income ($)",
        ]
    ].copy()

    df = df.rename(
        columns={
            "Code": "sa2_code",
            "Label": "sa2",
            "Year": "year",
            "Median employee income ($)": "median_employee_income",
        }
    )

    df["year"] = df["year"].astype(int)

    df["median_employee_income"] = pd.to_numeric(
        df["median_employee_income"],
        errors="coerce",
    )

    df = df.sort_values(["sa2_code", "year"]).reset_index(drop=True)

    return df


def validate_data(df):
    """Run basic data-quality checks."""

    print("\nValidation:")
    print(f"Rows: {len(df):,}")
    print(f"Unique SA2s: {df['sa2_code'].nunique():,}")
    print(f"Years: {sorted(df['year'].unique())}")

    duplicates = df.duplicated(
        subset=["sa2_code", "year"]
    ).sum()

    print(f"Duplicate SA2-year rows: {duplicates}")

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nMissing income by year:")
    print(
        df.groupby("year")["median_employee_income"]
        .apply(lambda s: s.isna().sum())
        .to_string()
    )

    print("\nIncome summary:")
    print(
        df["median_employee_income"]
        .describe()
        .to_string()
    )


def save_data(df):
    OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_DATA, index=False)


def main():
    print("Loading ABS income data...")
    df = load_income_data()

    print("Preparing SA2 income data...")
    df = prepare_income_data(df)

    validate_data(df)

    print("\nSaving cleaned dataset...")
    save_data(df)

    print(f"Saved to: {OUTPUT_DATA}")


if __name__ == "__main__":
    main()