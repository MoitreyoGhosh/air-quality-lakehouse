"""
evaluator.py

Model Evaluation Metrics
"""

import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


class Evaluator:
    """
    Evaluate regression models.
    """

    @staticmethod
    def evaluate(
        y_true,
        y_pred
    ):
        """
        Compute regression metrics.
        """

        mae = mean_absolute_error(
            y_true,
            y_pred
        )

        mse = mean_squared_error(
            y_true,
            y_pred
        )

        rmse = np.sqrt(mse)

        r2 = r2_score(
            y_true,
            y_pred
        )

        # Avoid division by zero
        mask = y_true != 0

        if np.any(mask):
            mape = (
                np.mean(
                    np.abs(
                        (y_true[mask] - y_pred[mask])
                        / y_true[mask]
                    )
                )
                * 100
            )
        else:
            mape = np.nan

        return {
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "R2": r2,
            "MAPE": mape,
        }

    # =====================================================
    # Pretty Print
    # =====================================================

    @staticmethod
    def print_metrics(metrics):

        print("=" * 60)
        print("MODEL EVALUATION")
        print("=" * 60)

        for key, value in metrics.items():

            if isinstance(value, float):
                print(f"{key:<10}: {value:.4f}")
            else:
                print(f"{key:<10}: {value}")


if __name__ == "__main__":

    # Demo

    y_true = np.array([100, 120, 150, 170, 200])

    y_pred = np.array([98, 118, 152, 168, 205])

    metrics = Evaluator.evaluate(
        y_true,
        y_pred
    )

    Evaluator.print_metrics(metrics)