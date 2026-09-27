from pathlib import Path
import zipfile
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ZIP_PATH = PROJECT_ROOT / "data" / "raw" / "2021_GCP_SA2.zip"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "rental_sa2_2021.csv"


RENT_BANDS = [
    ("R_1_74_Tot", 1, 74),
    ("R_75_99_Tot", 75, 99),
    ("R_100_149_Tot", 100, 149),
    ("R_150_199_Tot", 150, 199),
    ("R_200_224_Tot", 200, 224),
    ("R_225_274_Tot", 225, 274),
    ("R_275_349_Tot", 275, 349),
    ("R_350_449_Tot", 350, 449),
    ("R_450_549_Tot", 450, 549),
    ("R_550_649_Tot", 550, 649),
    ("R_650_749_Tot", 650, 749),
    ("R_750_849_Tot", 750, 849),
    ("R_850_949_Tot", 850, 949),
]


def estimate_grouped_median(row):
    """
    Estimate the median weekly rent from grouped Census rent bands.

    The open-ended $950+ band cannot be interpolated reliably, so if
    the median falls in that band, the result is set to missing.
    """

    frequencies = []

    for column, lower, upper in RENT_BANDS:
        frequency = pd.to_numeric(row[column], errors="coerce")

        if pd.isna(frequency):
            frequency = 0

        frequencies.append((lower, upper, float(frequency)))

    total = sum(freq for _, _, freq in frequencies)

    if total <= 0:
        return pd.NA

    target = total / 2
    cumulative = 0

    for lower, upper, frequency in frequencies:
        previous_cumulative = cumulative
        cumulative += frequency

        if cumulative >= target:
            if frequency <= 0:
                return pd.NA

            # Linear interpolation within the grouped interval.
            estimate = lower + (
                (target - previous_cumulative) / frequency
            ) * (upper - lower)

            return round(estimate, 2)

    # Median falls in the $950+ open-ended category.
    return pd.NA


def main():
    print("Loading Census G40 rental data...")

    internal_path = (
        "2021 Census GCP Statistical Area 2 for AUS/"
        "2021Census_G40_AUST_SA2.csv"
    )

    with zipfile.ZipFile(ZIP_PATH) as z:
        with z.open(internal_path) as f:
            df = pd.read_csv(f)

    print(f"Raw shape: {df.shape}")

    required_columns = (
        ["SA2_CODE_2021"]
        + [column for column, _, _ in RENT_BANDS]
        + ["Rent_ns_Tot", "Tot_Tot"]
    )

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing expected columns: {missing_columns}"
        )

    # Keep only the fields needed for the rental measure.
    result = df[required_columns].copy()

    # SA2 codes are identifiers, so keep them as strings.
    result["sa2_code"] = (
        result["SA2_CODE_2021"]
        .astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .str.zfill(9)
    )

    # Convert rent-band counts to numeric.
    for column, _, _ in RENT_BANDS:
        result[column] = pd.to_numeric(
            result[column], errors="coerce"
        ).fillna(0)

    result["Rent_ns_Tot"] = pd.to_numeric(
        result["Rent_ns_Tot"], errors="coerce"
    ).fillna(0)

    result["Tot_Tot"] = pd.to_numeric(
        result["Tot_Tot"], errors="coerce"
    )

    # Number of rented dwellings with a stated weekly rent.
    result["rented_dwellings"] = (
        result[[column for column, _, _ in RENT_BANDS]]
        .sum(axis=1)
    )

    # Estimate median weekly rent.
    result["estimated_median_weekly_rent"] = result.apply(
        estimate_grouped_median,
        axis=1
    )

    # Keep the final analytical fields.
    result = result[
        [
            "sa2_code",
            "rented_dwellings",
            "Rent_ns_Tot",
            "Tot_Tot",
            "estimated_median_weekly_rent",
        ]
    ]

    # Remove invalid/aggregate SA2 codes.
    result = result[
        result["sa2_code"].str.fullmatch(r"\d{9}", na=False)
    ].copy()

    result = result.drop_duplicates(
        subset=["sa2_code"]
    )

    result = result.sort_values("sa2_code")

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"Saved: {OUTPUT_PATH}")
    print(f"Rows: {len(result):,}")
    print(
        "Median estimates available:",
        result["estimated_median_weekly_rent"].notna().sum()
    )
    print(
        "Median estimates missing:",
        result["estimated_median_weekly_rent"].isna().sum()
    )

    print("\nPreview:")
    print(result.head(10).to_string(index=False))


if __name__ == "__main__":
    main()