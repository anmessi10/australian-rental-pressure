from pathlib import Path

import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestRegressor


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_model_features_2021.csv"
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

    # ---------------------------------------------------------
    # 1. Correlation between predictors and target
    # ---------------------------------------------------------

    print("\nCORRELATION WITH RENTAL TARGET")
    print("-" * 70)

    correlations = (
        df[FEATURES + [TARGET]]
        .corr(numeric_only=True)[TARGET]
        .drop(TARGET)
        .sort_values(key=abs, ascending=False)
    )

    print(correlations.to_string())

    # ---------------------------------------------------------
    # 2. Correlation between predictors
    # ---------------------------------------------------------

    print("\n\nPREDICTOR CORRELATION MATRIX")
    print("-" * 70)

    predictor_corr = df[FEATURES].corr()

    print(predictor_corr.round(3).to_string())

    # ---------------------------------------------------------
    # 3. Train Random Forest
    # ---------------------------------------------------------

    print("\n\nTRAINING RANDOM FOREST")
    print("-" * 70)

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
        min_samples_leaf=3,
    )

    model.fit(X, y)

    # ---------------------------------------------------------
    # 4. Built-in feature importance
    # ---------------------------------------------------------

    print("\nBUILT-IN RANDOM FOREST IMPORTANCE")
    print("-" * 70)

    impurity_importance = pd.DataFrame({
        "feature": FEATURES,
        "importance": model.feature_importances_,
    }).sort_values(
        "importance",
        ascending=False,
    )

    print(
        impurity_importance.to_string(
            index=False
        )
    )

    # ---------------------------------------------------------
    # 5. Permutation importance
    # ---------------------------------------------------------

    print("\nPERMUTATION IMPORTANCE")
    print("-" * 70)

    permutation = permutation_importance(
        model,
        X,
        y,
        n_repeats=10,
        random_state=42,
        n_jobs=-1,
        scoring="r2",
    )

    permutation_importance_df = pd.DataFrame({
        "feature": FEATURES,
        "importance_mean": permutation.importances_mean,
        "importance_std": permutation.importances_std,
    }).sort_values(
        "importance_mean",
        ascending=False,
    )

    print(
        permutation_importance_df.to_string(
            index=False
        )
    )

    # ---------------------------------------------------------
    # 6. Save diagnostic results
    # ---------------------------------------------------------

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "model_diagnostics_2021.csv"
    )

    diagnostic_output = (
        permutation_importance_df
        .merge(
            correlations.rename("target_correlation"),
            left_on="feature",
            right_index=True,
        )
        .merge(
            impurity_importance.rename(
                columns={"importance": "impurity_importance"}
            ),
            on="feature",
        )
    )

    diagnostic_output.to_csv(
        output_path,
        index=False,
    )

    print(f"\nSaved diagnostics: {output_path}")


if __name__ == "__main__":
    main()