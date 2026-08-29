# File: /home/susan/mof-co2-adsorption/mof_models.py
# Create this new Python file in the repository root.
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np


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