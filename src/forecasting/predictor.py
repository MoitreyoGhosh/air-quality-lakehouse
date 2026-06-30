"""
predictor.py

Model Prediction Module

Responsibilities
----------------
1. Load trained models
2. Predict on new datasets
3. Predict on single observations
"""

from pathlib import Path
import joblib
import pandas as pd


class Predictor:
    """
    Load trained models and perform predictions.
    """

    def __init__(self):

        self.model_dir = Path("models")

    # =====================================================
    # Load Model
    # =====================================================

    def load_model(self, filename: str):

        model_path = self.model_dir / filename

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        return joblib.load(model_path)

    # =====================================================
    # Predict DataFrame
    # =====================================================

    def predict(
        self,
        model,
        X: pd.DataFrame
    ):

        return model.predict(X)

    # =====================================================
    # Predict Single Record
    # =====================================================

    def predict_single(
        self,
        model,
        sample
    ):

        return model.predict([sample])[0]

    # =====================================================
    # Complete Prediction Pipeline
    # =====================================================

    def run(
        self,
        model_name: str,
        X: pd.DataFrame
    ):

        model = self.load_model(model_name)

        predictions = self.predict(
            model,
            X
        )

        result = X.copy()

        result["prediction"] = predictions

        return result


if __name__ == "__main__":

    print("=" * 60)
    print("Predictor Module")
    print("=" * 60)
    print("Import this module after training a model.")