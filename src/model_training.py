"""
Model Training Module

Trains RandomForest classifier for match outcome prediction.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MatchPredictor:
    """
    RandomForest-based match outcome predictor
    """
    
    def __init__(self):
        """Initialize the predictor"""
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.is_trained = False
        
    def train(self, X: pd.DataFrame, y: pd.Series, 
              test_size: float = 0.2, tune_hyperparameters: bool = True):
        """
        Train the RandomForest model
        
        Args:
            X: Feature DataFrame
            y: Labels Series
            test_size: Proportion of data for testing
            tune_hyperparameters: Whether to perform grid search
        """
        logger.info("="*70)
        logger.info("TRAINING RANDOMFOREST MODEL")
        logger.info("="*70)
        
        # Store feature names
        self.feature_names = list(X.columns)
        logger.info(f"\nFeatures ({len(self.feature_names)}): {self.feature_names}")
        
        # Split data
        logger.info(f"\nSplitting data (test_size={test_size})...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        logger.info(f"Training set: {len(X_train)} samples")
        logger.info(f"Test set: {len(X_test)} samples")
        
        # Scale features
        logger.info("\nScaling features...")
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        if tune_hyperparameters:
            logger.info("\nPerforming hyperparameter tuning...")
            self.model = self._tune_hyperparameters(X_train_scaled, y_train)
        else:
            logger.info("\nTraining with default parameters...")
            self.model = RandomForestClassifier(
                n_estimators=200,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        logger.info("\n" + "="*70)
        logger.info("MODEL EVALUATION")
        logger.info("="*70)
        
        # Training accuracy
        y_train_pred = self.model.predict(X_train_scaled)
        train_accuracy = accuracy_score(y_train, y_train_pred)
        logger.info(f"\nTraining Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
        
        # Test accuracy
        y_test_pred = self.model.predict(X_test_scaled)
        test_accuracy = accuracy_score(y_test, y_test_pred)
        logger.info(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
        
        # Classification report
        logger.info("\nClassification Report:")
        logger.info("\n" + classification_report(
            y_test, y_test_pred,
            target_names=['Away Win', 'Draw', 'Home Win']
        ))
        
        # Confusion matrix
        logger.info("Confusion Matrix:")
        cm = confusion_matrix(y_test, y_test_pred)
        logger.info(f"\n{cm}")
        logger.info("\n(Rows: Actual, Columns: Predicted)")
        logger.info("Order: Away Win, Draw, Home Win")
        
        # Feature importance
        logger.info("\n" + "-"*70)
        logger.info("FEATURE IMPORTANCE")
        logger.info("-"*70)
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for _, row in feature_importance.iterrows():
            logger.info(f"{row['feature']:.<30} {row['importance']:.4f}")
        
        # Cross-validation
        logger.info("\n" + "-"*70)
        logger.info("CROSS-VALIDATION (5-fold)")
        logger.info("-"*70)
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train, cv=5, scoring='accuracy'
        )
        logger.info(f"CV Scores: {cv_scores}")
        logger.info(f"Mean CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        self.is_trained = True
        
        # Return metrics
        return {
            'train_accuracy': float(train_accuracy),
            'test_accuracy': float(test_accuracy),
            'cv_mean': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std()),
            'feature_importance': feature_importance.to_dict('records'),
            'confusion_matrix': cm.tolist(),
            'classification_report': classification_report(
                y_test, y_test_pred,
                target_names=['Away Win', 'Draw', 'Home Win'],
                output_dict=True
            )
        }
    
    def _tune_hyperparameters(self, X_train, y_train):
        """
        Perform grid search for hyperparameter tuning
        
        Args:
            X_train: Training features
            y_train: Training labels
            
        Returns:
            Best model
        """
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [15, 20, 25, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        rf = RandomForestClassifier(random_state=42, n_jobs=-1)
        
        grid_search = GridSearchCV(
            rf, param_grid, cv=3, scoring='accuracy',
            n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        logger.info(f"\nBest parameters: {grid_search.best_params_}")
        logger.info(f"Best CV score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict match outcomes
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Predicted labels
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict match outcome probabilities
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Probability matrix (n_samples, 3)
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)
    
    def save(self, model_path: str = 'models/match_predictor.pkl',
             scaler_path: str = 'models/feature_scaler.pkl',
             metrics_path: str = 'models/model_metrics.json'):
        """
        Save model, scaler, and metrics
        
        Args:
            model_path: Path to save model
            scaler_path: Path to save scaler
            metrics_path: Path to save metrics
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        # Create directory
        Path(model_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save model and scaler
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        
        # Save metadata
        metadata = {
            'feature_names': self.feature_names,
            'model_type': 'RandomForestClassifier',
            'n_estimators': int(self.model.n_estimators),
            'max_depth': int(self.model.max_depth) if self.model.max_depth else None,
        }
        
        # Read existing metrics if they exist
        if Path(metrics_path).exists():
            with open(metrics_path, 'r') as f:
                existing_metrics = json.load(f)
            metadata.update(existing_metrics)
        
        with open(metrics_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"\n[OK] Model saved to {model_path}")
        logger.info(f"[OK] Scaler saved to {scaler_path}")
        logger.info(f"[OK] Metadata saved to {metrics_path}")
    
    def load(self, model_path: str = 'models/match_predictor.pkl',
             scaler_path: str = 'models/feature_scaler.pkl',
             metrics_path: str = 'models/model_metrics.json'):
        """
        Load model, scaler, and metrics
        
        Args:
            model_path: Path to model file
            scaler_path: Path to scaler file
            metrics_path: Path to metrics file
        """
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        
        with open(metrics_path, 'r') as f:
            metadata = json.load(f)
            self.feature_names = metadata['feature_names']
        
        self.is_trained = True
        logger.info(f"[OK] Model loaded from {model_path}")


def main():
    """
    Train and save the model
    """
    print("="*70)
    print("RANDOMFOREST MODEL TRAINING")
    print("="*70)
    
    # Load features and labels
    print("\nLoading training data...")
    X = pd.read_csv('data/processed/training_features.csv')
    y = pd.read_csv('data/processed/training_labels.csv')['outcome']
    
    print(f"Loaded {len(X)} samples with {len(X.columns)} features")
    print(f"Label distribution:\n{y.value_counts()}")
    
    # Initialize and train
    predictor = MatchPredictor()
    metrics = predictor.train(X, y, test_size=0.2, tune_hyperparameters=False)
    
    # Save metrics first
    with open('models/model_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Then save model (which will update metrics with feature_names)
    predictor.save()
    
    print("\n" + "="*70)
    print("[OK] Model training complete!")
    print("="*70)
    print(f"Test Accuracy: {metrics['test_accuracy']*100:.2f}%")
    print(f"CV Accuracy: {metrics['cv_mean']*100:.2f}% (+/- {metrics['cv_std']*2*100:.2f}%)")


if __name__ == "__main__":
    main()

# Made with Bob
