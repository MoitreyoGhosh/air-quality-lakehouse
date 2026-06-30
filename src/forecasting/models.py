"""
models.py

Machine Learning Model Factory
"""

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    ExtraTreesRegressor,
)
from sklearn.tree import DecisionTreeRegressor


class ModelFactory:
    """
    Factory class for creating forecasting models.
    """

    @staticmethod
    def linear_regression():
        return LinearRegression()

    @staticmethod
    def decision_tree(
        random_state: int = 42
    ):
        return DecisionTreeRegressor(
            random_state=random_state
        )

    @staticmethod
    def random_forest(
        n_estimators: int = 200,
        random_state: int = 42
    ):
        return RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1
        )

    @staticmethod
    def gradient_boosting(
        random_state: int = 42
    ):
        return GradientBoostingRegressor(
            random_state=random_state
        )

    @staticmethod
    def extra_trees(
        n_estimators: int = 200,
        random_state: int = 42
    ):
        return ExtraTreesRegressor(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1
        )

    @staticmethod
    def available_models():
        """
        Return all supported models.
        """

        return {
            "Linear Regression": ModelFactory.linear_regression(),
            "Decision Tree": ModelFactory.decision_tree(),
            "Random Forest": ModelFactory.random_forest(),
            "Gradient Boosting": ModelFactory.gradient_boosting(),
            "Extra Trees": ModelFactory.extra_trees(),
        }


if __name__ == "__main__":

    print("=" * 60)
    print("AVAILABLE MODELS")
    print("=" * 60)

    for name, model in ModelFactory.available_models().items():
        print(f"{name:20} -> {model}")