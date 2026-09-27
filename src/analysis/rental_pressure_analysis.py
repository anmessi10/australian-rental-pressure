from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INDEX_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "historical_rental_pressure_index_2019_2023.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_pressure_analysis_2019_2023.csv"
)

FIGURES_DIR = PROJECT_ROOT / "results" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def main():

    print("Loading Historical Rental Pressure Index...")

    df = pd.read_csv(INDEX_PATH)

    print(f"States/territories: {len(df)}")

    # Sort by index value for analysis
    df = df.sort_values(
        "historical_rental_pressure_index",
        ascending=False
    ).reset_index(drop=True)

    # Add position for descriptive purposes.
    # This is NOT an overall judgement about housing conditions.
    df["index_position"] = range(1, len(df) + 1)

    print("\nHISTORICAL RENTAL PRESSURE INDEX")
    print("-" * 100)

    print(
        df.to_string(index=False)
    )

    # Save analysis dataset
    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nSaved: {OUTPUT_PATH}"
    )

    # ---------------------------------------------------------
    # Index distribution
    # ---------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.barh(
        df["state"],
        df["historical_rental_pressure_index"]
    )

    plt.xlabel(
        "Historical Rental Pressure Index (0–100)"
    )

    plt.ylabel("State / Territory")

    plt.title(
        "Historical Rental Pressure Index, 2019–2023"
    )

    plt.gca().invert_yaxis()

    plt.tight_layout()

    figure_path = (
        FIGURES_DIR
        / "historical_rental_pressure_index.png"
    )

    plt.savefig(
        figure_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved figure: {figure_path}"
    )


if __name__ == "__main__":
    main()