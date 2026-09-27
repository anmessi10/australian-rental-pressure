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
    / "housing_supply_state_2025_26.csv"
)


def load_data():
    """Load the SA2 housing-supply dataset."""

    return pd.read_csv(
        INPUT_DATA,
        dtype={"sa2_code": str},
    )


def aggregate_to_state(df):
    """
    Aggregate SA2 housing approvals to state/territory level.

    The period covered is July 2025 to June 2026.
    """

    df = df.copy()

    # Calculate total approved dwellings by state.
    state_totals = (
        df.groupby("state", as_index=False)
        .agg(
            population=(
                "population",
                "sum",
            ),
            approved_dwellings_12m=(
                "approved_dwellings_12m",
                "sum",
            ),
            sa2_count=(
                "sa2_code",
                "nunique",
            ),
        )
    )

    # Calculate approvals per 1,000 residents.
    state_totals["approvals_per_1000"] = (
        state_totals["approved_dwellings_12m"]
        / state_totals["population"]
        * 1000
    )

    # Sort by the supply rate for easier inspection.
    state_totals = state_totals.sort_values(
        "approvals_per_1000",
        ascending=False,
    ).reset_index(drop=True)

    return state_totals


def calculate_sa2_distribution(df):
    """
    Calculate distribution statistics for approvals
    across SA2 regions within each state.
    """

    distribution = (
        df.groupby("state")["approvals_per_1000"]
        .agg(
            sa2_median="median",
            sa2_mean="mean",
            sa2_min="min",
            sa2_max="max",
        )
        .reset_index()
    )

    return distribution


def validate_data(df):
    print("\nValidation:")

    print(
        f"States/territories: "
        f"{df['state'].nunique()}"
    )

    print(
        f"Duplicate states: "
        f"{df['state'].duplicated().sum()}"
    )

    print("\nMissing values:")

    print(df.isna().sum())

    print("\nState-level housing supply:")

    print(
        df.to_string(index=False)
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

    print("Loading housing supply dataset...")

    df = load_data()

    print(
        "Calculating state-level housing supply..."
    )

    state_totals = aggregate_to_state(df)

    validate_data(state_totals)

    print(
        "\nSA2-level distribution by state:"
    )

    distribution = calculate_sa2_distribution(
        df
    )

    print(
        distribution.to_string(index=False)
    )

    print("\nSaving state-level results...")

    save_data(state_totals)

    print(
        f"Saved to: {OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()