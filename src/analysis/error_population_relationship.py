from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DIAGNOSTICS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "model_prediction_diagnostics_2021.csv"
)

POPULATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "population_sa2_clean.csv"
)

FIGURES_DIR = PROJECT_ROOT / "results" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def main():

    diagnostics = pd.read_csv(DIAGNOSTICS_PATH)
    population = pd.read_csv(POPULATION_PATH)

    diagnostics["sa2_code"] = (
        diagnostics["sa2_code"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(9)
    )

    population["sa2_code"] = (
        population["sa2_code"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(9)
    )

    pop_2021 = (
        population[population["year"] == 2021]
        [["sa2_code", "population"]]
        .drop_duplicates("sa2_code")
    )

    merged = diagnostics.merge(
        pop_2021,
        on="sa2_code",
        how="left"
    )

    # Correlation between population and absolute prediction error
    correlation = merged[
        ["population", "absolute_error"]
    ].corr().iloc[0, 1]

    print("\nPOPULATION VS PREDICTION ERROR")
    print("-" * 60)
    print(
        f"Pearson correlation: {correlation:.3f}"
    )

    # Population groups
    merged["population_group"] = pd.cut(
        merged["population"],
        bins=[0, 500, 1000, 5000, 10000, float("inf")],
        labels=[
            "<500",
            "500-999",
            "1,000-4,999",
            "5,000-9,999",
            "10,000+"
        ],
        include_lowest=True
    )

    summary = (
        merged
        .groupby("population_group", observed=False)
        .agg(
            observations=("absolute_error", "count"),
            mean_absolute_error=("absolute_error", "mean"),
            median_absolute_error=("absolute_error", "median")
        )
        .reset_index()
    )

    print("\nERROR BY POPULATION GROUP")
    print("-" * 80)
    print(summary.to_string(index=False))

    # Scatter plot
    plt.figure(figsize=(8, 7))

    plt.scatter(
        merged["population"],
        merged["absolute_error"],
        alpha=0.55
    )

    plt.xlabel("SA2 population (2021)")
    plt.ylabel("Absolute prediction error")
    plt.title(
        "Random Forest Prediction Error vs SA2 Population"
    )

    plt.tight_layout()

    output_path = (
        FIGURES_DIR
        / "prediction_error_vs_population.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"\nSaved figure: {output_path}"
    )


if __name__ == "__main__":
    main()