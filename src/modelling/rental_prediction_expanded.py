from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
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
    / "rental_model_results_expanded_2021.csv"
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

    print("Loading expanded modelling dataset...")
    df = pd.read_csv(DATA_PATH)

    print(f"Rows: {len(df):,}")

    X = df[FEATURES]
    y = df[TARGET]

    print("\nFEATURES")
    print("-" * 60)
    for feature in FEATURES:
        print(feature)

    print("\nTARGET")
    print("-" * 60)
    print(TARGET)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    print("\nTRAIN / TEST SPLIT")
    print("-" * 60)
    print(f"Training observations: {len(X_train):,}")
    print(f"Testing observations:  {len(X_test):,}")

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=300,
            random_state=42,
            n_jobs=-1,
            min_samples_leaf=3,
        ),
    }

    results = []

    for name, model in models.items():

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(
            y_test,
            predictions,
        )

        # Calculate RMSE manually for compatibility
        # with the installed scikit-learn version.
        rmse = mean_squared_error(
            y_test,
            predictions,
        ) ** 0.5

        r2 = r2_score(
            y_test,
            predictions,
        )

        results.append({
            "model": name,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        })

    results_df = pd.DataFrame(results)

    print("\nMODEL PERFORMANCE")
    print("-" * 75)
    print(results_df.to_string(index=False))

    # Train Random Forest for feature importance.
    rf = models["Random Forest"]

    importance = pd.DataFrame({
        "feature": FEATURES,
        "importance": rf.feature_importances_,
    }).sort_values(
        "importance",
        ascending=False,
    )

    print("\nRANDOM FOREST FEATURE IMPORTANCE")
    print("-" * 75)
    print(importance.to_string(index=False))

    results_df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"\nSaved model results: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()