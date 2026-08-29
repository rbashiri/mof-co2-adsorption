
# File: /home/susan/mof-co2-adsorption/notebook/modeling/test_training_data.ipynb
# Add the following content in ONE CODE CELL.
# If needed, install once from the VS Code terminal:
# python -m pip install ipytest

import numpy as np
import ipytest
import pytest

from sklearn.datasets import make_regression
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

# Absolute imports from the reusable module being tested.
from mof_models import (
    build_dummy_model,
    build_gradient_boosting_search,
    build_linear_model,
    build_random_forest_model,
    build_ridge_model,
    evaluate_regression,
)




@pytest.fixture
def regression_data():
    """Small deterministic data only for fast model tests."""
    X, y = make_regression(
        n_samples=80,
        n_features=4,
        noise=0.1,
        random_state=12345,
    )
    return X, y


def test_dummy_model_uses_mean_strategy():
    model = build_dummy_model()

    assert isinstance(model, DummyRegressor)
    assert model.strategy == "mean"


def test_linear_model_is_linear_regression():
    model = build_linear_model()

    assert isinstance(model, LinearRegression)


def test_ridge_model_contains_scaler_and_ridge():
    model = build_ridge_model(alpha=1.0)

    assert isinstance(model, Pipeline)
    assert model.named_steps["scaler"] is not None
    assert model.named_steps["model"].alpha == 1.0


@pytest.mark.parametrize(
    "model_builder",
    [
        build_dummy_model,
        build_linear_model,
        build_ridge_model,
        build_random_forest_model,
    ],
)
def test_baseline_models_fit_and_predict(model_builder, regression_data):
    X, y = regression_data
    model = model_builder()

    model.fit(X, y)
    predictions = model.predict(X)

    assert predictions.shape == y.shape
    assert np.all(np.isfinite(predictions))


def test_random_forest_configuration():
    model = build_random_forest_model(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
    )

    assert isinstance(model, RandomForestRegressor)
    assert model.n_estimators == 100
    assert model.max_depth == 10
    assert model.min_samples_split == 5
    assert model.min_samples_leaf == 2
    assert model.random_state == 12345
    assert model.n_jobs == 1


def test_evaluate_regression_returns_correct_metrics():
    y_true = np.array([1.0, 2.0, 3.0])
    predictions = np.array([1.0, 2.0, 4.0])

    metrics = evaluate_regression(y_true, predictions)

    assert set(metrics) == {"mae", "rmse", "r2"}
    assert metrics["mae"] == pytest.approx(1 / 3)
    assert metrics["rmse"] == pytest.approx(np.sqrt(1 / 3))
    assert metrics["r2"] == pytest.approx(0.5)


def test_gradient_boosting_grid_search_configuration():
    search = build_gradient_boosting_search()

    assert isinstance(search, GridSearchCV)
    assert isinstance(search.estimator, GradientBoostingRegressor)
    assert search.estimator.random_state == 12345
    assert search.scoring == "neg_mean_absolute_error"
    assert search.n_jobs == 1
    assert search.cv.n_splits == 5
    assert search.cv.shuffle is True
    assert search.cv.random_state == 12345

    assert search.param_grid["n_estimators"] == [100, 200]
    assert search.param_grid["learning_rate"] == [0.05, 0.1]
    assert search.param_grid["max_depth"] == [2, 3]


def test_gradient_boosting_grid_search_fits_small_grid(regression_data):
    X, y = regression_data

    # Five fits only: appropriate for a test, unlike the full production grid.
    small_grid = {
        "n_estimators": [10],
        "learning_rate": [0.1],
        "max_depth": [2],
        "min_samples_split": [2],
        "min_samples_leaf": [1],
    }

    search = build_gradient_boosting_search(param_grid=small_grid)
    search.fit(X, y)

    assert isinstance(search.best_estimator_, GradientBoostingRegressor)
    assert np.isfinite(search.best_score_)
    assert search.best_params_ == {
        "learning_rate": 0.1,
        "max_depth": 2,
        "min_samples_leaf": 1,
        "min_samples_split": 2,
        "n_estimators": 10,
    }


ipytest.run("-q")