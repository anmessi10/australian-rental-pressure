from pathlib import Path
import zipfile
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ZIP_PATH = PROJECT_ROOT / "data" / "raw" / "2021_GCP_SA2.zip"

BASE_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_model_dataset_2021.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_model_features_2021.csv"
)

G02_PATH = (
    "2021 Census GCP Statistical Area 2 for AUS/"
    "2021Census_G02_AUST_SA2.csv"
)


def main():

    print("Loading base modelling dataset...")
    base = pd.read_csv(BASE_DATA_PATH)

    base["sa2_code"] = (
        base["sa2_code"]
        .astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .str.zfill(9)
    )

    print(f"Base rows: {len(base):,}")

    print("\nLoading Census G02...")
    with zipfile.ZipFile(ZIP_PATH) as z:
        with z.open(G02_PATH) as f:
            g02 = pd.read_csv(f)

    g02["sa2_code"] = (
        g02["SA2_CODE_2021"]
        .astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .str.zfill(9)
    )

    feature_columns = [
        "sa2_code",
        "Median_age_persons",
        "Median_mortgage_repay_monthly",
        "Median_tot_prsnl_inc_weekly",
        "Median_tot_fam_inc_weekly",
        "Average_num_psns_per_bedroom",
        "Median_tot_hhd_inc_weekly",
        "Average_household_size",
    ]

    g02 = g02[feature_columns]

    print(f"G02 rows: {len(g02):,}")

    print("\nMerging datasets...")
    df = base.merge(
        g02,
        on="sa2_code",
        how="left",
        validate="one_to_one",
    )

    print(f"Merged rows: {len(df):,}")

    # Predictors used by the expanded model.
    model_features = [
        "population",
        "median_employee_income",
        "Median_age_persons",
        "Median_mortgage_repay_monthly",
        "Median_tot_prsnl_inc_weekly",
        "Median_tot_fam_inc_weekly",
        "Average_num_psns_per_bedroom",
        "Median_tot_hhd_inc_weekly",
        "Average_household_size",
    ]

    target = "estimated_median_weekly_rent"

    required_columns = ["sa2_code", target] + model_features

    df = df[required_columns].copy()

    # Remove observations with missing predictor/target values.
    before = len(df)

    df = df.dropna(
        subset=[target] + model_features
    )

    # Population must be positive for this modelling task.
    df = df[df["population"] > 0]

    print(f"Rows before final filtering: {before:,}")
    print(f"Final rows: {len(df):,}")

    print("\nMissing values:")
    print(df.isna().sum().to_string())

    print("\nDuplicate SA2 codes:")
    print(df["sa2_code"].duplicated().sum())

    print("\nModel features:")
    for feature in model_features:
        print(f"  - {feature}")

    print(f"\nTarget:")
    print(f"  - {target}")

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()