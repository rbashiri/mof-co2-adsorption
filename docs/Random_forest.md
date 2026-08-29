# Random Forest Key Parameters Guide

Looking at your notebook, here are the **critical parameters** to consider when building a Random Forest model as a solid base structure.

---

## 🌲 Core Parameters (Most Critical)

| Parameter | Your Current Value | Recommendation |
|---|---|---|
| `n_estimators` | 100 | Start with 100–200 |
| `max_depth` | 15 | **Too deep** → overfitting risk. Start with `None` or 10–15 |
| `random_state` | 12345 | ✅ Keep for reproducibility |
| `n_jobs` | 1 | Use `-1` to use all CPU cores |

---

## ⚠️ Overfitting Control Parameters (Important)

| Parameter | Purpose | Recommended Start |
|---|---|---|
| `min_samples_split` | Min samples required to split a node | `2` (default) or `5` |
| `min_samples_leaf` | Min samples required at a leaf node | `1` (default) or `2` |
| `max_features` | Features considered per split | `"sqrt"` (default, good for regression) |

---

## 🚫 What Random Forest Does NOT Need

Unlike Ridge or Linear Regression:

- ❌ **No scaling required** — tree-based models split on thresholds, so feature scale is irrelevant
- ❌ **No regularization parameter (alpha)** — overfitting is controlled via tree depth and leaf size
- ❌ **No `StandardScaler` pipeline** — unnecessary overhead

---

## ✅ Recommended Base Structure

```python
from sklearn.ensemble import RandomForestRegressor

model_rf_base = RandomForestRegressor(
    n_estimators=100,        # Start here, tune up to 300
    max_depth=None,          # Let trees grow fully first, then constrain
    min_samples_split=2,     # Default — tune later
    min_samples_leaf=1,      # Default — tune later
    max_features="sqrt",     # Good general default for regression
    random_state=12345,      # Reproducibility
    n_jobs=-1                # Use all CPU cores
)

model_rf_base.fit(X_train, y_train)
```

---

## 🔍 Parameter Tuning Priority Order

```
1. max_depth           ← HIGHEST IMPACT on overfitting
2. n_estimators        ← More trees = more stable, but diminishing returns
3. min_samples_leaf    ← Controls leaf size, reduces noise sensitivity
4. min_samples_split   ← Controls when a node can be split
5. max_features        ← Usually "sqrt" works well, rarely needs changing
```

---

## 📌 Key Observation From Your Notebook

In your current code you have:

```python
# ⚠️ Issues spotted:
n_jobs=1      # Only uses 1 CPU core — slow!
max_depth=15  # Fixed depth before tuning — may cause overfitting
```

Your Grid Search confirmed `max_depth` in range `[8, 10, 12]` performed better
than your initial `15`, which is evidence that **`max_depth` was your biggest tuning lever**.

---

## 🔧 Grid Search Template

```python
from sklearn.model_selection import GridSearchCV, KFold

param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [8, 10, 12],
    "min_samples_split": [3, 5, 8],
    "min_samples_leaf": [1, 2, 4]
}

cv_method = KFold(n_splits=5, shuffle=True, random_state=12345)

grid_search_rf = GridSearchCV(
    estimator=model_rf_base,
    param_grid=param_grid,
    scoring="neg_mean_absolute_error",
    cv=cv_method,
    n_jobs=-1,
    verbose=1
)

grid_search_rf.fit(X_train, y_train)

print("Best parameters:", grid_search_rf.best_params_)
print("Best CV MAE:", -grid_search_rf.best_score_)

best_model_rf = grid_search_rf.best_estimator_
```

---

## 📊 Evaluate Best Model

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

predicted_valid = best_model_rf.predict(X_valid)

mae  = mean_absolute_error(y_valid, predicted_valid)
rmse = np.sqrt(mean_squared_error(y_valid, predicted_valid))
r2   = r2_score(y_valid, predicted_valid)

print(f"Validation MAE:  {mae:.6f}")
print(f"Validation RMSE: {rmse:.6f}")
print(f"Validation R²:   {r2:.6f}")
```

---

## 🧱 Suggested Workflow

```
1. Build base model (max_depth=None, defaults)
         ↓
2. Check train vs validation gap (overfitting check)
         ↓
3. Tune max_depth first
         ↓
4. Then tune min_samples_leaf + min_samples_split
         ↓
5. Finally increase n_estimators if needed
         ↓
6. Evaluate once on test set — never tune after this step
```