"""
trainer.py

Model Training Pipeline
"""

from pathlib import Path
import joblib

from src.forecasting.models import ModelFactory
from src.forecasting.evaluator import Evaluator


class ModelTrainer:
    """
    Train and save forecasting models.
    """

    def __init__(self):

        self.model_dir = Path("models")
        self.model_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # =====================================================
    # Train Model
    # =====================================================

    def train(
        self,
        model,
        X_train,
        y_train
    ):

        model.fit(
            X_train,
            y_train
        )

        return model

    # =====================================================
    # Evaluate Model
    # =====================================================

    def evaluate(
        self,
        model,
        X_test,
        y_test
    ):

        predictions = model.predict(X_test)

        return Evaluator.evaluate(
            y_test,
            predictions
        )

    # =====================================================
    # Save Model
    # =====================================================

    def save_model(
        self,
        model,
        filename
    ):

        path = self.model_dir / filename

        joblib.dump(
            model,
            path
        )

        print(f"Model saved to: {path}")

    # =====================================================
    # Complete Pipeline
    # =====================================================

    def train_model(
        self,
        model_name,
        X_train,
        X_test,
        y_train,
        y_test
    ):

        models = ModelFactory.available_models()

        if model_name not in models:
            raise ValueError(
                f"Unknown model: {model_name}"
            )

        model = models[model_name]

        print("=" * 70)
        print(f"Training: {model_name}")
        print("=" * 70)

        model = self.train(
            model,
            X_train,
            y_train
        )

        metrics = self.evaluate(
            model,
            X_test,
            y_test
        )

        filename = (
            model_name.lower()
            .replace(" ", "_")
            + ".joblib"
        )

        self.save_model(
            model,
            filename
        )

        print("\nEvaluation Metrics")

        for key, value in metrics.items():
            print(f"{key:10}: {value:.4f}")

        return model, metrics