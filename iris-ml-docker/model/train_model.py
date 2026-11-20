import os
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def train():
    print("=" * 60)
    print("Step 1: Loading Iris dataset...")
    print("=" * 60)
    iris = load_iris()
    X = iris.data
    y = iris.target
    target_names = iris.target_names
    feature_names = iris.feature_names
    print(f"Features: {feature_names}")
    print(f"Target classes: {list(target_names)}")
    print(f"Dataset shape: {X.shape[0]} samples, {X.shape[1]} features")

    print("\n" + "=" * 60)
    print("Step 2: Splitting dataset (80% train, 20% test, random_state=42)...")
    print("=" * 60)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set size: {X_train.shape[0]} samples")
    print(f"Testing set size:  {X_test.shape[0]} samples")

    print("\n" + "=" * 60)
    print("Step 3: Training RandomForestClassifier (n_estimators=100, random_state=42)...")
    print("=" * 60)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    print("Model training completed successfully.")

    print("\n" + "=" * 60)
    print("Step 4: Generating predictions on test set...")
    print("=" * 60)
    y_pred = clf.predict(X_test)

    print("\n" + "=" * 60)
    print("Step 5: Calculating Model Accuracy...")
    print("=" * 60)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}% ({accuracy:.4f})")

    print("\n" + "=" * 60)
    print("Step 6: Displaying Classification Report...")
    print("=" * 60)
    report = classification_report(y_test, y_pred, target_names=target_names)
    print(report)

    print("=" * 60)
    print("Step 7: Saving trained model to model.joblib in project root...")
    print("=" * 60)
    # Determine project root (one directory up from model/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    model_save_path = os.path.join(project_root, "model.joblib")

    joblib.dump(clf, model_save_path)
    print(f"Trained model saved successfully to: {model_save_path}")
    print(f"File size: {os.path.getsize(model_save_path)} bytes")
    print("=" * 60)


if __name__ == "__main__":
    train()

