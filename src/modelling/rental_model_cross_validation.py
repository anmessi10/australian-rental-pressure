from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.model_selection import KFold, cross_validate
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_model_features_2021.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_model_cross_validation_2021.csv"
)


FEATURES = [
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

TARGET = "estimated_median_weekly_rent"


def main():

    print("Loading modelling dataset...")

    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    print(f"Observations: {len(df):,}")
    print(f"Features: {len(FEATURES)}")

    models = {
        "Linear Regression": LinearRegression(),

        "Random Forest": RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1,
            min_samples_leaf=3,
        ),
    }

    # Same five folds are used for both models.
    cv = KFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    scoring = {
        "MAE": "neg_mean_absolute_error",
        "RMSE": "neg_root_mean_squared_error",
        "R2": "r2",
    }

    all_results = []

    for name, model in models.items():

        print(f"\nEvaluating: {name}")

        scores = cross_validate(
            model,
            X,
            y,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
        )

        fold_mae = -scores["test_MAE"]
        fold_rmse = -scores["test_RMSE"]
        fold_r2 = scores["test_R2"]

        for fold in range(5):

            all_results.append({
                "model": name,
                "fold": fold + 1,
                "MAE": fold_mae[fold],
                "RMSE": fold_rmse[fold],
                "R2": fold_r2[fold],
            })

        print(
            f"Mean MAE:  {fold_mae.mean():.3f}"
        )
        print(
            f"Mean RMSE: {fold_rmse.mean():.3f}"
        )
        print(
            f"Mean R2:   {fold_r2.mean():.3f}"
        )

    results_df = pd.DataFrame(all_results)

    print("\n\nCROSS-VALIDATION RESULTS")
    print("-" * 80)
    print(results_df.to_string(index=False))

    print("\n\nSUMMARY BY MODEL")
    print("-" * 80)

    summary = (
        results_df
        .groupby("model")
        .agg(
            MAE_mean=("MAE", "mean"),
            MAE_std=("MAE", "std"),
            RMSE_mean=("RMSE", "mean"),
            RMSE_std=("RMSE", "std"),
            R2_mean=("R2", "mean"),
            R2_std=("R2", "std"),
        )
        .reset_index()
    )

    print(summary.to_string(index=False))

    results_df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()