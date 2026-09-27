from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "housing_supply_sa2_2025_26.csv"
)

OUTPUT_FIGURE = (
    PROJECT_ROOT
    / "results"
    / "figures"
    / "sa2_approval_rate_distribution.png"
)


def main():

    print("Loading data...")

    df = pd.read_csv(INPUT_DATA)

    # Remove SA2s without a calculated approval rate.
    rates = df["approvals_per_1000"].dropna()

    print(f"SA2s included: {len(rates):,}")

    print(
        f"Median approval rate: "
        f"{rates.median():.2f} per 1,000"
    )

    print(
        f"Mean approval rate: "
        f"{rates.mean():.2f} per 1,000"
    )

    print("Creating histogram...")

    plt.figure(figsize=(10, 6))

    plt.hist(
        rates,
        bins=50,
    )

    plt.xlabel(
        "New residential dwelling approvals per 1,000 residents"
    )

    plt.ylabel(
        "Number of SA2 regions"
    )

    plt.title(
        "Distribution of New Residential Dwelling Approval Rates\n"
        "Australian SA2 Regions, July 2025–June 2026"
    )

    plt.tight_layout()

    OUTPUT_FIGURE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(
        OUTPUT_FIGURE,
        dpi=300,
    )

    plt.close()

    print(
        f"Saved figure to: {OUTPUT_FIGURE}"
    )


if __name__ == "__main__":
    main()