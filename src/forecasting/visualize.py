"""
visualize.py

Visualization utilities for forecasting models.

Responsibilities
----------------
1. Actual vs Predicted
2. Residual Plot
3. Feature Importance
4. Prediction Error Distribution
5. Forecast Trend
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid")

plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 11


class ForecastVisualizer:

    # =====================================================
    # Actual vs Predicted
    # =====================================================

    @staticmethod
    def actual_vs_predicted(
        y_true,
        y_pred
    ):

        plt.figure()

        plt.plot(
            y_true.values,
            label="Actual",
            linewidth=2
        )

        plt.plot(
            y_pred,
            label="Predicted",
            linewidth=2
        )

        plt.title("Actual vs Predicted")

        plt.xlabel("Observations")
        plt.ylabel("Target")

        plt.legend()

        plt.tight_layout()

        plt.show()

    # =====================================================
    # Residual Plot
    # =====================================================

    @staticmethod
    def residual_plot(
        y_true,
        y_pred
    ):

        residuals = y_true - y_pred

        plt.figure()

        sns.scatterplot(
            x=y_pred,
            y=residuals
        )

        plt.axhline(
            0,
            color="red",
            linestyle="--"
        )

        plt.title("Residual Plot")

        plt.xlabel("Predicted")

        plt.ylabel("Residual")

        plt.tight_layout()

        plt.show()

    # =====================================================
    # Error Distribution
    # =====================================================

    @staticmethod
    def error_distribution(
        y_true,
        y_pred
    ):

        errors = y_true - y_pred

        plt.figure()

        sns.histplot(
            errors,
            kde=True,
            bins=30,
            color="steelblue"
        )

        plt.title("Prediction Error Distribution")

        plt.tight_layout()

        plt.show()

    # =====================================================
    # Feature Importance
    # =====================================================

    @staticmethod
    def feature_importance(
        model,
        feature_names
    ):

        if not hasattr(model, "feature_importances_"):

            print(
                "Feature importance not available for this model."
            )

            return

        importance = pd.DataFrame({

            "Feature": feature_names,

            "Importance": model.feature_importances_

        })

        importance = importance.sort_values(
            "Importance",
            ascending=False
        )

        plt.figure(figsize=(10, 6))

        sns.barplot(
            data=importance,
            x="Importance",
            y="Feature",
            palette="viridis"
        )

        plt.title("Feature Importance")

        plt.tight_layout()

        plt.show()

    # =====================================================
    # Forecast Trend
    # =====================================================

    @staticmethod
    def forecast(
        dataframe: pd.DataFrame,
        datetime_column: str,
        prediction_column: str
    ):

        plt.figure()

        sns.lineplot(
            data=dataframe,
            x=datetime_column,
            y=prediction_column,
            linewidth=2,
            color="royalblue"
        )

        plt.title("Forecast")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.show()


if __name__ == "__main__":

    print("=" * 60)
    print("Forecast Visualization Module")
    print("=" * 60)
    print("Import this module after model prediction.")