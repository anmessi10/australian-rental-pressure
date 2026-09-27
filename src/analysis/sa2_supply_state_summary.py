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
    / "sa2_supply_state_summary_2025_26.csv"
)


def main():

    print("Loading data...")

    df = pd.read_csv(INPUT_DATA)

    # Only include SA2s with a calculated approval rate.
    df = df.dropna(
        subset=["approvals_per_1000"]
    )

    print(
        f"SA2s included: {len(df):,}"
    )

    print("\nCalculating state-level SA2 statistics...")

    summary = (
        df.groupby("state")["approvals_per_1000"]
        .agg(
            sa2_count="count",
            mean="mean",
            median="median",
            minimum="min",
            percentile_25=lambda x: x.quantile(0.25),
            percentile_75=lambda x: x.quantile(0.75),
            maximum="max",
        )
        .reset_index()
    )

    summary = summary.sort_values(
        "median",
        ascending=False,
    )

    # Round rates for readability.
    rate_columns = [
        "mean",
        "median",
        "minimum",
        "percentile_25",
        "percentile_75",
        "maximum",
    ]

    summary[rate_columns] = summary[rate_columns].round(2)

    print("\nSA2 approval-rate summary by state:")
    print(
        summary.to_string(index=False)
    )

    OUTPUT_DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary.to_csv(
        OUTPUT_DATA,
        index=False,
    )

    print(
        f"\nSaved summary to: {OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()