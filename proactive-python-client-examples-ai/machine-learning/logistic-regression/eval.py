import os
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

# Load the saved model
print("Loading the saved logistic regression model...")
model_path = 'models/logistic_regression_model.pkl'  # Adjust path if necessary
model = joblib.load(model_path)

# Load the test dataset
print("Loading the test dataset...")
X_test = pd.read_csv('dataset/cifar10-csv/test.csv', header=0)  # Change to `header=None` if there's no header row

# Preprocess the test dataset
print("Preprocessing test data...")
# Ensure all feature columns are numeric, coercing errors to NaN
X_test.iloc[:, :-1] = X_test.iloc[:, :-1].apply(pd.to_numeric, errors='coerce')
# Optionally, drop rows with NaN values
X_test = X_test.dropna()

# Make predictions on the test set
print("Making predictions on the test set...")
y_pred = model.predict(X_test)

# Create the 'predictions' directory if it doesn't exist
predictions_dir = 'predictions'
os.makedirs(predictions_dir, exist_ok=True)

# Save predictions to a text file within the 'predictions' folder
predictions_file = os.path.join(predictions_dir, 'logistic_regression.txt')
print(f"Saving predictions to '{predictions_file}'...")
with open(predictions_file, 'w') as f:
    for pred in y_pred:
        f.write(f"{pred}\n")

print(f"Predictions were successfully saved to '{predictions_file}'.")

print("Model prediction and evaluation on test data complete.")
