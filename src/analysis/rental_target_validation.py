from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RENTAL_PATH = PROJECT_ROOT / "data" / "processed" / "rental_sa2_2021.csv"
POPULATION_PATH = PROJECT_ROOT / "data" / "processed" / "population_sa2_clean.csv"


def main():
    rental = pd.read_csv(
        RENTAL_PATH,
        dtype={"sa2_code": str}
    )

    population = pd.read_csv(
        POPULATION_PATH,
        dtype={"sa2_code": str}
    )

    population_2021 = population[
        population["year"] == 2021
    ][
        ["sa2_code", "state", "sa2", "population"]
    ].copy()

    population_2021["sa2_code"] = (
        population_2021["sa2_code"]
        .astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .str.zfill(9)
    )

    df = rental.merge(
        population_2021,
        on="sa2_code",
        how="inner"
    )

    print("\nMISSING RENT TARGETS")
    print("-" * 60)

    missing = df[
        df["estimated_median_weekly_rent"].isna()
    ].copy()

    print(f"Missing: {len(missing)}")

    print("\nPopulation of missing-rent SA2s:")
    print(
        missing["population"]
        .describe()
        .to_string()
    )

    print("\nLargest missing-rent SA2s:")
    print(
        missing
        .sort_values("population", ascending=False)
        [["state", "sa2", "population", "rented_dwellings", "Tot_Tot"]]
        .head(20)
        .to_string(index=False)
    )

    print("\nRENT TARGET DISTRIBUTION")
    print("-" * 60)

    valid = df[
        df["estimated_median_weekly_rent"].notna()
    ].copy()

    print(
        valid["estimated_median_weekly_rent"]
        .describe(
            percentiles=[
                0.01,
                0.05,
                0.10,
                0.90,
                0.95,
                0.99
            ]
        )
        .to_string()
    )

    print("\nLOWEST RENT ESTIMATES")
    print("-" * 60)

    print(
        valid
        .sort_values("estimated_median_weekly_rent")
        [["state", "sa2", "population",
          "rented_dwellings",
          "estimated_median_weekly_rent"]]
        .head(20)
        .to_string(index=False)
    )

    print("\nHIGHEST RENT ESTIMATES")
    print("-" * 60)

    print(
        valid
        .sort_values(
            "estimated_median_weekly_rent",
            ascending=False
        )
        [["state", "sa2", "population",
          "rented_dwellings",
          "estimated_median_weekly_rent"]]
        .head(20)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()