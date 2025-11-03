"""
Machine Learning model training script
Module: plagiarism_checker/backend_api/model.py

This script trains a logistic regression model on plagiarism dataset
and saves it for later use in the Flask API.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, classification_report, confusion_matrix, roc_auc_score
)
import joblib
import os


def train_model(
    dataset_file="plagiarism_dataset.csv",
    model_file="plagiarism_model.pkl",
    test_size=0.2,
    random_state=42,
    model_type="logistic"
):
    """
    Train logistic regression or SVM model for plagiarism classification
    
    Args:
        dataset_file (str): Path to training dataset CSV
        model_file (str): Path to save trained model
        test_size (float): Proportion of data for testing
        random_state (int): Random seed for reproducibility
        model_type (str): "logistic" or "svm"
    
    Returns:
        dict: Training results including metrics
    """
    
    print("=" * 60)
    print("🤖 PLAGIARISM DETECTION MODEL TRAINING")
    print("=" * 60)
    
    # Check if dataset exists
    if not os.path.exists(dataset_file):
        print(f"❌ Error: Dataset file '{dataset_file}' not found!")
        print("   Run 'python data_prep.py' first to create the dataset.")
        return None
    
    print(f"\n📂 Loading dataset from: {dataset_file}")
    df = pd.read_csv(dataset_file)
    print(f"   ✓ Loaded {len(df)} samples")
    
    # Prepare features and labels
    X = df[["Similarity"]]
    y = df["Label"]
    
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total samples: {len(df)}")
    print(f"   Plagiarized (1): {(y == 1).sum()}")
    print(f"   Original (0): {(y == 0).sum()}")
    print(f"   Similarity - Mean: {X['Similarity'].mean():.4f}, Std: {X['Similarity'].std():.4f}")
    
    # Split data
    print(f"\n📋 Splitting data (test_size={test_size})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    print(f"   ✓ Training set: {len(X_train)} samples")
    print(f"   ✓ Test set: {len(X_test)} samples")
    
    # Train model
    print(f"\n🚀 Training {model_type} Regression model...")
    
    if model_type.lower() == "logistic":
        model = LogisticRegression(
            random_state=random_state,
            max_iter=1000,
            solver='lbfgs'
        )
    elif model_type.lower() == "svm":
        model = SVC(
            random_state=random_state,
            kernel='rbf',
            probability=True
        )
    else:
        print(f"❌ Unknown model type: {model_type}")
        return None
    
    model.fit(X_train, y_train)
    print("   ✓ Model trained successfully")
    
    # Make predictions
    print(f"\n📈 Evaluating model on test set...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\n✅ Model Evaluation Metrics:")
    print(f"   Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"   Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"   F1-Score:  {f1:.4f}")
    print(f"   ROC-AUC:   {roc_auc:.4f}")
    
    # Classification report
    print(f"\n📊 Classification Report:")
    print(classification_report(
        y_test, y_pred,
        target_names=["Original", "Plagiarized"]
    ))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n🔢 Confusion Matrix:")
    print(f"   True Negatives:  {cm[0][0]} | False Positives: {cm[0][1]}")
    print(f"   False Negatives: {cm[1][0]} | True Positives:  {cm[1][1]}")
    
    # Save model
    print(f"\n💾 Saving model to: {model_file}")
    joblib.dump(model, model_file)
    print(f"   ✓ Model saved successfully")
    
    # Print model info
    if model_type.lower() == "logistic":
        print(f"\n🔧 Model Details:")
        print(f"   Type: Logistic Regression")
        print(f"   Coefficients: {model.coef_[0]}")
        print(f"   Intercept: {model.intercept_[0]}")
    
    print("\n" + "=" * 60)
    print("✨ MODEL TRAINING COMPLETE!")
    print("=" * 60)
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "model": model,
        "X_test": X_test,
        "y_test": y_test
    }


def load_model(model_file="plagiarism_model.pkl"):
    """
    Load a trained model from file
    
    Args:
        model_file (str): Path to model file
    
    Returns:
        Trained model object or None if not found
    """
    if not os.path.exists(model_file):
        print(f"❌ Model file '{model_file}' not found!")
        return None
    
    try:
        model = joblib.load(model_file)
        print(f"✓ Model loaded from {model_file}")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return None


if __name__ == "__main__":
    # Train with Logistic Regression
    results = train_model(model_type="logistic")
    
    if results:
        print("\n📝 To use this model in the Flask app, ensure:")
        print("   1. model.py is in the same directory as app.py")
        print("   2. plagiarism_model.pkl is generated in backend_api/")
        print("   3. Run 'python app.py' to start the API")