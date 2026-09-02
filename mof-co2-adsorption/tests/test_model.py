import unittest
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class TestModel(unittest.TestCase):
    def setUp(self):
        self.X, self.y = make_regression(
            n_samples=100,
            n_features=10,
            noise=0.1,
            random_state=42,
        )
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.model = Pipeline([
            ('scaler', StandardScaler()),
            ('rf', RandomForestRegressor(random_state=42))
        ])
        self.param_grid = {
            'rf__n_estimators': [50, 100],
            'rf__max_depth': [None, 10, 20],
            'rf__min_samples_split': [2, 5]
        }
        self.grid_search = GridSearchCV(self.model, self.param_grid, cv=5)

    def test_model_performance(self):
        self.grid_search.fit(self.X_train, self.y_train)
        predictions = self.grid_search.predict(self.X_test)
        r2 = r2_score(self.y_test, predictions)
        self.assertTrue(np.isfinite(r2))
        self.assertGreater(r2, 0.0)

if __name__ == '__main__':
    unittest.main()