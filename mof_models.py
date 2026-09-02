# File: /home/susan/mof-co2-adsorption/mof_models.py
# Create this new Python file in the repository root.
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd


def build_dummy_model():
    """Create the mean-prediction baseline."""
    return DummyRegressor(strategy="mean")


def build_linear_model():
    """Create the linear-regression baseline."""
    return LinearRegression()


def build_ridge_model(alpha=1.0):
    """Create Ridge regression with feature scaling."""
    return Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=alpha)),
    ])


def build_random_forest_model(
    n_estimators=100,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features="sqrt",
):
    """Create a reproducible Random Forest regressor."""
    return RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        random_state=12345,
        n_jobs=1,
    )


def build_gradient_boosting_search(param_grid=None):
    """Create a single-worker Gradient Boosting GridSearchCV object."""
    if param_grid is None:
        param_grid = {
            "n_estimators": [100, 200],
            "learning_rate": [0.05, 0.1],
            "max_depth": [2, 3],
        }

    cv_method = KFold(
        n_splits=5,
        shuffle=True,
        random_state=12345,
    )

    return GridSearchCV(
        estimator=GradientBoostingRegressor(random_state=12345),
        param_grid=param_grid,
        scoring="neg_mean_absolute_error",
        cv=cv_method,
        n_jobs=1,
        verbose=0,
        error_score="raise",
    )


def evaluate_regression(y_true, predictions):
    """Return standard regression metrics in one consistent dictionary."""
    mae = mean_absolute_error(y_true, predictions)
    mse = mean_squared_error(y_true, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, predictions)
    
    return {"mae": mae, "rmse": rmse, "r2": r2}


def split_target_data(dataframe, feature_columns, target_column, seed=12345):
    """Return reproducible 60/20/20 splits for one target column."""
    selected_features = dataframe[feature_columns].copy()
    selected_target = dataframe[target_column].copy()

    X_train, X_temp, y_train, y_temp = train_test_split(
        selected_features,
        selected_target,
        test_size=0.4,
        shuffle=True,
        random_state=seed,
    )
    X_valid, X_test, y_valid, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.5,
        shuffle=True,
        random_state=seed,
    )
    return X_train, X_valid, X_test, y_train, y_valid, y_test


def train_and_evaluate_random_forest(
    X_train, X_valid, X_test, y_train, y_valid, y_test, rf_params
):
    """Fit one Random Forest and return metrics and predictions for all splits."""
    model = RandomForestRegressor(**rf_params)
    model.fit(X_train, y_train)

    predictions = {
        "train": model.predict(X_train),
        "valid": model.predict(X_valid),
        "test": model.predict(X_test),
    }
    actual_values = {
        "train": y_train,
        "valid": y_valid,
        "test": y_test,
    }
    metrics = {
        split_name: evaluate_regression(actual_values[split_name], predictions[split_name])
        for split_name in actual_values
    }

    return {
        "model": model,
        "metrics": metrics,
        "predictions": predictions,
    }


def evaluate_target_columns(
    dataframe, feature_columns, target_columns, rf_params, seed=12345
):
    """Evaluate fixed-parameter Random Forest models across target columns."""
    results = {}
    summary_rows = []

    for target_column in target_columns:
        splits = split_target_data(dataframe, feature_columns, target_column, seed=seed)
        evaluation = train_and_evaluate_random_forest(*splits, rf_params)
        results[target_column] = evaluation

        row = {"target": target_column}
        for split_name, split_metrics in evaluation["metrics"].items():
            for metric_name, metric_value in split_metrics.items():
                row[f"{split_name}_{metric_name}"] = metric_value
        row["train_valid_r2_gap"] = row["train_r2"] - row["valid_r2"]
        row["valid_test_r2_gap"] = row["valid_r2"] - row["test_r2"]
        summary_rows.append(row)

    return results, pd.DataFrame(summary_rows)