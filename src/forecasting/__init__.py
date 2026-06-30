"""
Environmental Intelligence Lakehouse
Forecasting Package
===================================

This package provides the complete machine learning
pipeline for environmental forecasting.

Modules
-------
dataset.py
    Load and prepare datasets from the lakehouse.

preprocessing.py
    Data cleaning, feature engineering, and train/test split.

models.py
    Machine learning model definitions.

trainer.py
    Model training and persistence.

predictor.py
    Load trained models and generate predictions.

evaluator.py
    Evaluate model performance using standard metrics.

visualize.py
    Visualization utilities for forecasts and model evaluation.
"""

from .dataset import DatasetLoader
from .preprocessing import DataPreprocessor
from .models import ModelFactory
from .trainer import ModelTrainer
from .predictor import Predictor
from .evaluator import Evaluator

__version__ = "1.0.0"

__all__ = [
    "DatasetLoader",
    "DataPreprocessor",
    "ModelFactory",
    "ModelTrainer",
    "Predictor",
    "Evaluator",
]