from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "housing_supply_sa2_2025_26.csv"
)

OUTPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sa2_supply_analysis_2025_26.csv"
)


def load_data():
    """Load the SA2 housing-supply dataset."""

    return pd.read_csv(
        INPUT_DATA,
        dtype={"sa2_code": str},
    )


def calculate_supply_statistics(df):
    """
    Calculate summary statistics for approvals per
    1,000 residents at the SA2 level.
    """

    statistics = (
        df["approvals_per_1000"]
        .describe()
        .to_frame()
        .T
    )

    return statistics


def calculate_percentiles(df):
    """
    Calculate useful percentile thresholds for the
    distribution of SA2 approval rates.
    """

    percentiles = (
        df["approvals_per_1000"]
        .quantile(
            [
                0.10,
                0.25,
                0.50,
                0.75,
                0.90,
            ]
        )
        .reset_index()
    )

    percentiles.columns = [
        "percentile",
        "approvals_per_1000",
    ]

    return percentiles


def identify_high_supply_areas(df):
    """
    Identify SA2s in the top 10% of the approval-rate
    distribution.
    """

    threshold = df["approvals_per_1000"].quantile(0.90)

    high_supply = df[
        df["approvals_per_1000"] >= threshold
    ].copy()

    high_supply = high_supply.sort_values(
        "approvals_per_1000",
        ascending=False,
    )

    return high_supply, threshold


def identify_low_supply_areas(df):
    """
    Identify SA2s in the bottom 10% of the approval-rate
    distribution.
    """

    threshold = df["approvals_per_1000"].quantile(0.10)

    low_supply = df[
        df["approvals_per_1000"] <= threshold
    ].copy()

    low_supply = low_supply.sort_values(
        "approvals_per_1000",
        ascending=True,
    )

    return low_supply, threshold


def validate_data(df):
    print("\nValidation:")

    print(
        f"SA2 regions: {len(df):,}"
    )

    print(
        f"States/territories: "
        f"{df['state'].nunique()}"
    )

    print(
        f"Duplicate SA2 codes: "
        f"{df['sa2_code'].duplicated().sum()}"
    )

    print("\nMissing values:")

    print(df.isna().sum())

    print("\nSupply-rate summary:")

    print(
        calculate_supply_statistics(df)
        .to_string(index=False)
    )


def save_data(df):
    OUTPUT_DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_DATA,
        index=False,
    )


def main():

    print("Loading SA2 housing-supply dataset...")

    df = load_data()

    validate_data(df)

    print("\nPercentiles:")

    percentiles = calculate_percentiles(df)

    print(
        percentiles.to_string(index=False)
    )

    print("\nIdentifying high-supply SA2s...")

    high_supply, high_threshold = (
        identify_high_supply_areas(df)
    )

    print(
        f"90th percentile threshold: "
        f"{high_threshold:.2f} approvals per 1,000"
    )

    print(
        f"SA2s in top 10%: "
        f"{len(high_supply)}"
    )

    print("\nTop 10 highest approval rates:")

    print(
        high_supply[
            [
                "state",
                "sa2",
                "population",
                "approved_dwellings_12m",
                "approvals_per_1000",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\nIdentifying low-supply SA2s...")

    low_supply, low_threshold = (
        identify_low_supply_areas(df)
    )

    print(
        f"10th percentile threshold: "
        f"{low_threshold:.2f} approvals per 1,000"
    )

    print(
        f"SA2s in bottom 10%: "
        f"{len(low_supply)}"
    )

    print("\nLowest 10 approval rates:")

    print(
        low_supply[
            [
                "state",
                "sa2",
                "population",
                "approved_dwellings_12m",
                "approvals_per_1000",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\nSaving results...")

    save_data(df)

    print(
        f"Saved to: {OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()