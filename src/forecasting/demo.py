"""
demo.py

End-to-End Forecasting Demo

Pipeline:
---------
1. Load dataset from DuckDB
2. Preprocess data
3. Train Random Forest model
4. Evaluate model
5. Generate predictions
6. Visualize results
"""

from src.forecasting.dataset import DatasetLoader
from src.forecasting.preprocessing import DataPreprocessor
from src.forecasting.trainer import ModelTrainer
from src.forecasting.predictor import Predictor
from src.forecasting.visualize import ForecastVisualizer


def main():

    print("=" * 70)
    print("ENVIRONMENTAL FORECASTING DEMO")
    print("=" * 70)

    # =====================================================
    # Load Dataset
    # =====================================================

    print("\nLoading dataset...")

    loader = DatasetLoader()

    df = loader.prepare_dataset(
        target="aqi"
    )

    print(f"Dataset Shape : {df.shape}")

    # =====================================================
    # Preprocess
    # =====================================================

    print("\nPreprocessing...")

    pre = DataPreprocessor()

    X_train, X_test, y_train, y_test = pre.process(
        df,
        target="aqi"
    )

    print(f"Training Samples : {len(X_train)}")
    print(f"Testing Samples  : {len(X_test)}")

    # =====================================================
    # Train Model
    # =====================================================

    print("\nTraining Random Forest...")

    trainer = ModelTrainer()

    model, metrics = trainer.train_model(
        "Random Forest",
        X_train,
        X_test,
        y_train,
        y_test
    )

    print("\nModel Performance")

    for metric, value in metrics.items():
        print(f"{metric:<10}: {value:.4f}")

    # =====================================================
    # Prediction
    # =====================================================

    print("\nLoading saved model...")

    predictor = Predictor()

    model = predictor.load_model(
        "random_forest.joblib"
    )

    predictions = model.predict(X_test)

    print("\nPrediction Sample")

    print(predictions[:10])

    # =====================================================
    # Visualization
    # =====================================================

    print("\nGenerating plots...")

    ForecastVisualizer.actual_vs_predicted(
        y_test,
        predictions
    )

    ForecastVisualizer.residual_plot(
        y_test,
        predictions
    )

    ForecastVisualizer.error_distribution(
        y_test,
        predictions
    )

    ForecastVisualizer.feature_importance(
        model,
        X_train.columns
    )

    print("\nForecasting Demo Completed Successfully!")

    loader.close()


if __name__ == "__main__":
    main()