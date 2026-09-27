from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RENTAL_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_market_clean.csv"
)

POPULATION_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "population_sa2_clean.csv"
)

INCOME_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "income_sa2_clean.csv"
)

OUTPUT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "state_affordability_2019_2023.csv"
)


START_YEAR = 2019
END_YEAR = 2023


STATE_MAP = {
    "ACT": "Australian Capital Territory",
    "NSW": "New South Wales",
    "NT": "Northern Territory",
    "QLD": "Queensland",
    "SA": "South Australia",
    "TAS": "Tasmania",
    "VIC": "Victoria",
    "WA": "Western Australia",
}


def load_data():
    """Load the rental, population and income datasets."""

    rental = pd.read_csv(RENTAL_DATA)

    population = pd.read_csv(
        POPULATION_DATA,
        dtype={"sa2_code": str},
    )

    income = pd.read_csv(
        INCOME_DATA,
        dtype={"sa2_code": str},
    )

    return rental, population, income


def prepare_rental_data(df):
    """
    Convert monthly state-level rental data into
    annual mean median weekly rent for 2019-2023.
    """

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    df["year"] = df["date"].dt.year

    df = df[
        df["year"].between(START_YEAR, END_YEAR)
    ].copy()

    # Convert rental state abbreviations to full state names.
    df["state"] = df["state"].map(STATE_MAP)

    # Calculate the mean of the monthly median weekly rents
    # within each state and year.
    df = (
        df.groupby(
            ["state", "year"],
            as_index=False
        )["median_weekly_rent"]
        .mean()
    )

    df = df.rename(
        columns={
            "median_weekly_rent":
                "annual_mean_median_weekly_rent"
        }
    )

    return df


def prepare_population_data(df):
    """
    Aggregate SA2 population data to state level
    for each year from 2019-2023.
    """

    df = df.copy()

    df = df[
        df["year"].between(START_YEAR, END_YEAR)
    ].copy()

    df = (
        df.groupby(
            ["state", "year"],
            as_index=False
        )["population"]
        .sum()
    )

    return df


def prepare_income_data(df):
    """
    Attach state information to SA2 income records
    and calculate the median employee income across
    SA2s within each state and year.
    """

    df = df.copy()

    df = df[
        df["year"].between(START_YEAR, END_YEAR)
    ].copy()

    # Get the state associated with each SA2.
    state_lookup = (
        pd.read_csv(
            POPULATION_DATA,
            dtype={"sa2_code": str},
        )
        [
            [
                "sa2_code",
                "state",
            ]
        ]
        .drop_duplicates("sa2_code")
    )

    # Keep only the income fields needed for the analysis.
    df = df[
        [
            "sa2_code",
            "year",
            "median_employee_income",
        ]
    ].copy()

    # Attach state information to each SA2 income record.
    df = df.merge(
        state_lookup,
        on="sa2_code",
        how="left",
    )

    # Calculate the median employee income across
    # SA2s within each state and year.
    df = (
        df.groupby(
            [
                "state",
                "year",
            ]
        )["median_employee_income"]
        .median()
        .reset_index()
    )

    return df


def combine_data(
    rental,
    population,
    income,
):
    """
    Combine rental, population and income data
    and calculate rental affordability metrics.
    """

    # Combine rental and population data.
    df = rental.merge(
        population,
        on=[
            "state",
            "year",
        ],
        how="inner",
    )

    # Add state-level income.
    df = df.merge(
        income,
        on=[
            "state",
            "year",
        ],
        how="inner",
    )

    # Annualise the weekly rent.
    df["annualised_median_rent"] = (
        df["annual_mean_median_weekly_rent"] * 52
    )

    # Calculate annual rent as a percentage of
    # median employee income.
    df["rent_to_median_employee_income_pct"] = (
        df["annualised_median_rent"]
        / df["median_employee_income"]
        * 100
    )

    df = df.sort_values(
        [
            "year",
            "state",
        ]
    ).reset_index(drop=True)

    return df


def validate_data(df):
    """Run validation checks on the combined dataset."""

    print("\nValidation:")

    print(f"Rows: {len(df)}")

    print(
        f"States: "
        f"{df['state'].nunique()}"
    )

    print(
        f"Years: "
        f"{sorted(df['year'].unique())}"
    )

    print(
        "Duplicate state-year rows: "
        f"{df.duplicated(['state', 'year']).sum()}"
    )

    print("\nMissing values:")

    print(
        df.isna().sum()
    )

    print("\nState-year observations:")

    print(
        df.groupby("year")["state"]
        .count()
        .to_string()
    )

    print("\nIncome values by state:")

    print(
        df[
            [
                "state",
                "year",
                "median_employee_income",
            ]
        ]
        .to_string(index=False)
    )

    print("\nSample:")

    print(
        df.head(10)
        .to_string(index=False)
    )


def save_data(df):
    """Save the processed dataset."""

    OUTPUT_DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_DATA,
        index=False,
    )


def main():

    print("Loading datasets...")

    rental, population, income = load_data()

    print("Preparing rental data...")

    rental = prepare_rental_data(rental)

    print("Preparing population data...")

    population = prepare_population_data(
        population
    )

    print("Preparing income data...")

    income = prepare_income_data(
        income
    )

    print("Combining datasets...")

    df = combine_data(
        rental,
        population,
        income,
    )

    validate_data(df)

    print("\nSaving dataset...")

    save_data(df)

    print(
        f"Saved to: {OUTPUT_DATA}"
    )


if __name__ == "__main__":
    main()