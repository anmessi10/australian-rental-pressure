from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]


FILES = {
    "Rental market": (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "rental_market_clean.csv"
    ),
    "Population": (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "population_sa2_clean.csv"
    ),
    "Income": (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "income_sa2_clean.csv"
    ),
    "Housing approvals": (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "building_approvals_sa2_clean.csv"
    ),
}


def main():

    print("DATASET TIME-PERIOD CHECK")
    print("=" * 60)

    # ---------------------------------------------------------
    # RENTAL MARKET
    # ---------------------------------------------------------

    rental = pd.read_csv(
        FILES["Rental market"]
    )

    rental["date"] = pd.to_datetime(
        rental["date"]
    )

    print("\nRental market:")
    print(
        f"Start: {rental['date'].min().date()}"
    )
    print(
        f"End:   {rental['date'].max().date()}"
    )
    print(
        f"Months: {rental['date'].nunique()}"
    )

    # ---------------------------------------------------------
    # POPULATION
    # ---------------------------------------------------------

    population = pd.read_csv(
        FILES["Population"]
    )

    print("\nPopulation:")
    print(
        f"Start year: {population['year'].min()}"
    )
    print(
        f"End year:   {population['year'].max()}"
    )
    print(
        f"Years: {population['year'].nunique()}"
    )

    # ---------------------------------------------------------
    # INCOME
    # ---------------------------------------------------------

    income = pd.read_csv(
        FILES["Income"]
    )

    print("\nIncome:")
    print(
        f"Start year: {income['year'].min()}"
    )
    print(
        f"End year:   {income['year'].max()}"
    )
    print(
        f"Years: {income['year'].nunique()}"
    )

    # ---------------------------------------------------------
    # HOUSING APPROVALS
    # ---------------------------------------------------------

    housing = pd.read_csv(
        FILES["Housing approvals"]
    )

    housing["date"] = pd.to_datetime(
        housing["date"]
    )

    print("\nHousing approvals:")

    print(
        f"Start: {housing['date'].min().date()}"
    )

    print(
        f"End:   {housing['date'].max().date()}"
    )

    print(
        f"Months: {housing['date'].nunique()}"
    )

    # ---------------------------------------------------------
    # OVERLAPPING PERIOD
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("POTENTIAL COMMON PERIOD")
    print("=" * 60)

    print(
        "\nThe current datasets provide:"
    )

    print(
        "• Rental market: monthly data through April 2025"
    )

    print(
        "• Population: annual data through 2025"
    )

    print(
        "• Income: usable SA2 median employee income through 2023"
    )

    print(
        "• Housing approvals: July 2025–June 2026"
    )

    print(
        "\nThere is therefore no single period in the "
        "current datasets where all four measures overlap."
    )


if __name__ == "__main__":
    main()