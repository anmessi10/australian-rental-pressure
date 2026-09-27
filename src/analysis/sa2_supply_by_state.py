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
    / "sa2_approval_rate_by_state.png"
)


def main():

    print("Loading data...")

    df = pd.read_csv(INPUT_DATA)

    # Remove SA2s without a calculated approval rate.
    df = df.dropna(
        subset=["approvals_per_1000"]
    )

    states = [
        "New South Wales",
        "Victoria",
        "Queensland",
        "South Australia",
        "Western Australia",
        "Tasmania",
        "Northern Territory",
        "Australian Capital Territory",
    ]

    data = [
        df.loc[
            df["state"] == state,
            "approvals_per_1000",
        ]
        for state in states
    ]

    print("SA2 counts by state:")

    for state, values in zip(states, data):
        print(
            f"{state}: {len(values):,}"
        )

    print("\nCreating box plot...")

    plt.figure(figsize=(12, 7))

    plt.boxplot(
        data,
        tick_labels=[
            "NSW",
            "VIC",
            "QLD",
            "SA",
            "WA",
            "TAS",
            "NT",
            "ACT",
        ],
        showfliers=False,
    )

    plt.xlabel(
        "State / Territory"
    )

    plt.ylabel(
        "New residential dwelling approvals per 1,000 residents"
    )

    plt.title(
        "SA2-Level Distribution of New Residential Dwelling Approval Rates\n"
        "July 2025–June 2026"
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