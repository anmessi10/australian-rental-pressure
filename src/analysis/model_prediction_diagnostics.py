from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

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

FIGURES_DIR = PROJECT_ROOT / "results" / "figures"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)


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

    # Keep SA2 code for diagnostics
    sa2_info = df[["sa2_code"]].copy()

    X_train, X_test, y_train, y_test, info_train, info_test = train_test_split(
        X,
        y,
        sa2_info,
        test_size=0.20,
        random_state=42,
    )

    print(f"Training observations: {len(X_train):,}")
    print(f"Testing observations:  {len(X_test):,}")

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
        min_samples_leaf=3,
    )

    print("\nTraining Random Forest...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    print("\nMODEL PERFORMANCE")
    print("-" * 50)
    print(f"MAE:  {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"R2:   {r2:.3f}")

    # ---------------------------------------------------------
    # Create diagnostics dataframe
    # ---------------------------------------------------------

    diagnostics = info_test.copy()

    diagnostics["actual_rent"] = y_test.values
    diagnostics["predicted_rent"] = predictions

    diagnostics["residual"] = (
        diagnostics["actual_rent"]
        - diagnostics["predicted_rent"]
    )

    diagnostics["absolute_error"] = (
        diagnostics["residual"].abs()
    )

    diagnostics = diagnostics.sort_values(
        "absolute_error",
        ascending=False,
    )

    output_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "model_prediction_diagnostics_2021.csv"
    )

    diagnostics.to_csv(output_path, index=False)

    print(f"\nSaved diagnostics: {output_path}")

    # ---------------------------------------------------------
    # Actual vs predicted
    # ---------------------------------------------------------

    plt.figure(figsize=(8, 7))

    plt.scatter(
        y_test,
        predictions,
        alpha=0.55,
    )

    min_value = min(y_test.min(), predictions.min())
    max_value = max(y_test.max(), predictions.max())

    plt.plot(
        [min_value, max_value],
        [min_value, max_value],
        linestyle="--",
    )

    plt.xlabel("Actual estimated weekly rent")
    plt.ylabel("Predicted estimated weekly rent")
    plt.title("Random Forest: Actual vs Predicted Rent")

    plt.tight_layout()

    actual_predicted_path = (
        FIGURES_DIR
        / "random_forest_actual_vs_predicted.png"
    )

    plt.savefig(
        actual_predicted_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Saved figure: {actual_predicted_path}")

    # ---------------------------------------------------------
    # Residual plot
    # ---------------------------------------------------------

    plt.figure(figsize=(8, 7))

    plt.scatter(
        predictions,
        diagnostics["residual"],
        alpha=0.55,
    )

    plt.axhline(
        0,
        linestyle="--",
    )

    plt.xlabel("Predicted estimated weekly rent")
    plt.ylabel("Residual (actual - predicted)")
    plt.title("Random Forest Residuals")

    plt.tight_layout()

    residual_path = (
        FIGURES_DIR
        / "random_forest_residuals.png"
    )

    plt.savefig(
        residual_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Saved figure: {residual_path}")

    # ---------------------------------------------------------
    # Largest prediction errors
    # ---------------------------------------------------------

    print("\nLARGEST PREDICTION ERRORS")
    print("-" * 80)

    print(
        diagnostics[
            [
                "sa2_code",
                "actual_rent",
                "predicted_rent",
                "residual",
                "absolute_error",
            ]
        ]
        .head(15)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()