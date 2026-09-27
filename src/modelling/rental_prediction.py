from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_model_dataset_2021.csv"
)

RESULTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "rental_model_results_2021.csv"
)


def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5
    r2 = r2_score(y_test, predictions)

    return {
        "model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    }


def main():
    print("Loading modelling dataset...")

    df = pd.read_csv(
        DATA_PATH,
        dtype={"sa2_code": str}
    )

    print(f"Rows: {len(df):,}")

    # Predictors.
    features = [
        "population",
        "median_employee_income",
    ]

    # Target.
    target = "estimated_median_weekly_rent"

    X = df[features]
    y = df[target]

    print("\nFEATURES")
    print("-" * 50)
    print(features)

    print("\nTARGET")
    print("-" * 50)
    print(target)

    # 80/20 train-test split.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    print("\nTRAIN / TEST SPLIT")
    print("-" * 50)
    print(f"Training observations: {len(X_train):,}")
    print(f"Testing observations:  {len(X_test):,}")

    # Models.
    linear_model = LinearRegression()

    random_forest = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
        min_samples_leaf=3,
    )

    results = []

    results.append(
        evaluate_model(
            "Linear Regression",
            linear_model,
            X_train,
            X_test,
            y_train,
            y_test,
        )
    )

    results.append(
        evaluate_model(
            "Random Forest",
            random_forest,
            X_train,
            X_test,
            y_train,
            y_test,
        )
    )

    results_df = pd.DataFrame(results)

    print("\nMODEL PERFORMANCE")
    print("-" * 70)

    print(
        results_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.3f}"
        )
    )

    # Fit Random Forest again to obtain feature importance.
    random_forest.fit(X_train, y_train)

    feature_importance = pd.DataFrame(
        {
            "feature": features,
            "importance": random_forest.feature_importances_,
        }
    ).sort_values(
        "importance",
        ascending=False
    )

    print("\nRANDOM FOREST FEATURE IMPORTANCE")
    print("-" * 70)

    print(
        feature_importance.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    # Save model performance.
    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    results_df.to_csv(
        RESULTS_PATH,
        index=False
    )

    print(f"\nSaved model results: {RESULTS_PATH}")


if __name__ == "__main__":
    main()