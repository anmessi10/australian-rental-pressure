from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "population_pressure_2019_2023.csv"
)

OUTPUT_FIGURE = (
    PROJECT_ROOT
    / "results"
    / "figures"
    / "population_affordability_scatter.png"
)


def main():

    print("Loading population-pressure data...")

    df = pd.read_csv(INPUT_DATA)

    x = df["population_change_pct"]
    y = df[
        "affordability_change_percentage_points"
    ]

    correlation = x.corr(y)

    print(
        f"Pearson correlation: {correlation:.4f}"
    )

    print("Creating scatter plot...")

    plt.figure(figsize=(10, 7))

    plt.scatter(
        x,
        y,
    )

    # Add a simple linear trend line.
    slope, intercept = __import__(
        "numpy"
    ).polyfit(x, y, 1)

    x_line = __import__(
        "numpy"
    ).linspace(
        x.min(),
        x.max(),
        100,
    )

    y_line = (
        slope * x_line
        + intercept
    )

    plt.plot(
        x_line,
        y_line,
    )

    # Add state labels.
    for _, row in df.iterrows():

        plt.annotate(
            row["state"],
            (
                row["population_change_pct"],
                row[
                    "affordability_change_percentage_points"
                ],
            ),
            xytext=(5, 5),
            textcoords="offset points",
        )

    plt.axhline(
        0,
        linewidth=0.8,
    )

    plt.xlabel(
        "Population growth, 2019–2023 (%)"
    )

    plt.ylabel(
        "Change in rent-to-income ratio, 2019–2023 (percentage points)"
    )

    plt.title(
        "Population Growth and Change in Rental Affordability\n"
        "Australian States and Territories, 2019–2023"
    )

    plt.text(
        0.02,
        0.98,
        f"Pearson correlation = {correlation:.3f}",
        transform=plt.gca().transAxes,
        verticalalignment="top",
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