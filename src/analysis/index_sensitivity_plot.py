from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_pressure_index_sensitivity.csv"
)

OUTPUT_FIGURE = (
    PROJECT_ROOT
    / "results"
    / "figures"
    / "rental_pressure_index_sensitivity.png"
)


def main():

    print("Loading sensitivity results...")

    df = pd.read_csv(INPUT_DATA)

    # ---------------------------------------------------------
    # Sort states by the equal-weight scenario
    # ---------------------------------------------------------

    df = df.sort_values(
        "Equal",
        ascending=True,
    )

    # ---------------------------------------------------------
    # Create figure
    # ---------------------------------------------------------

    scenarios = [
        "Equal",
        "Rental-focused",
        "Population-focused",
        "Affordability-focused",
    ]

    fig, ax = plt.subplots(
        figsize=(12, 8)
    )

    y_positions = range(len(df))

    # ---------------------------------------------------------
    # Plot each scenario
    # ---------------------------------------------------------

    for scenario in scenarios:

        ax.plot(
            df[scenario],
            list(y_positions),
            marker="o",
            linewidth=2,
            label=scenario,
        )

    # ---------------------------------------------------------
    # Labels
    # ---------------------------------------------------------

    ax.set_yticks(
        list(y_positions)
    )

    ax.set_yticklabels(
        df["state"]
    )

    ax.set_xlabel(
        "Historical Rental Pressure Index (0–100)"
    )

    ax.set_ylabel(
        "State / Territory"
    )

    ax.set_title(
        "Historical Rental Pressure Index: "
        "Sensitivity to Component Weighting"
    )

    ax.set_xlim(
        0,
        100,
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.4,
    )

    ax.legend(
        title="Weighting scenario",
        loc="lower right",
    )

    plt.tight_layout()

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    OUTPUT_FIGURE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(
        OUTPUT_FIGURE,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"\nSaved figure to:\n{OUTPUT_FIGURE}"
    )


if __name__ == "__main__":
    main()