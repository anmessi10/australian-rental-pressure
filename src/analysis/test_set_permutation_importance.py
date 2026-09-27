from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance


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
    / "test_set_permutation_importance_2021.csv"
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

    # Use exactly the same split as Model 2.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    print(f"Training observations: {len(X_train):,}")
    print(f"Testing observations:  {len(X_test):,}")

    print("\nTraining Random Forest...")
    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
        min_samples_leaf=3,
    )

    model.fit(X_train, y_train)

    print("\nCalculating permutation importance on held-out test set...")

    permutation = permutation_importance(
        model,
        X_test,
        y_test,
        n_repeats=20,
        random_state=42,
        n_jobs=-1,
        scoring="r2",
    )

    results = pd.DataFrame({
        "feature": FEATURES,
        "importance_mean": permutation.importances_mean,
        "importance_std": permutation.importances_std,
    }).sort_values(
        "importance_mean",
        ascending=False,
    )

    print("\nHELD-OUT TEST-SET PERMUTATION IMPORTANCE")
    print("-" * 75)
    print(results.to_string(index=False))

    results.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()