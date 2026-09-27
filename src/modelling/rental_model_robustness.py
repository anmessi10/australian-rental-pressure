from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


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
    / "rental_model_robustness_2021.csv"
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

# Multiple random splits.
RANDOM_STATES = [1, 10, 21, 42, 52, 73, 100, 123, 202, 999]


def main():

    print("Loading modelling dataset...")

    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    print(f"Total observations: {len(df):,}")
    print(f"Number of splits: {len(RANDOM_STATES)}")

    results = []

    for random_state in RANDOM_STATES:

        print(f"\nRunning split: random_state={random_state}")

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=random_state,
        )

        model = RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1,
            min_samples_leaf=3,
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(
            y_test,
            predictions,
        )

        rmse = mean_squared_error(
            y_test,
            predictions,
        ) ** 0.5

        r2 = r2_score(
            y_test,
            predictions,
        )

        results.append({
            "random_state": random_state,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        })

        print(
            f"MAE={mae:.3f}, "
            f"RMSE={rmse:.3f}, "
            f"R2={r2:.3f}"
        )

    results_df = pd.DataFrame(results)

    print("\nROBUSTNESS RESULTS")
    print("-" * 70)
    print(results_df.to_string(index=False))

    print("\nSUMMARY")
    print("-" * 70)

    for metric in ["MAE", "RMSE", "R2"]:

        mean_value = results_df[metric].mean()
        std_value = results_df[metric].std()
        min_value = results_df[metric].min()
        max_value = results_df[metric].max()

        print(
            f"{metric}: "
            f"mean={mean_value:.3f}, "
            f"std={std_value:.3f}, "
            f"min={min_value:.3f}, "
            f"max={max_value:.3f}"
        )

    results_df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()