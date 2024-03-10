import os
import joblib

import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Set random seed for reproducibility
np.random.seed(0)

# Load the dataset
print("Loading the dataset...")
data = pd.read_csv('dataset/cifar10-csv/train.csv', header=0)  # Change to `header=None` if there's no header row

# Preprocess the dataset
print("Preprocessing data...")
# Ensure all feature columns are numeric, coercing errors to NaN
data.iloc[:, :-1] = data.iloc[:, :-1].apply(pd.to_numeric, errors='coerce')
# Optionally, drop rows with NaN values
data = data.dropna()

# Split the dataset into features and labels
X = data.iloc[:, :-1]  # All rows, all columns except the last one (features)
y = data.iloc[:, -1]   # All rows, only the last column (label)

# Split the data into training and validation sets
print("Splitting data into training and validation sets...")
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25)

# Create a logistic regression model with verbose output
print("Initializing and training the logistic regression model...")
model = LogisticRegression(max_iter=100, verbose=1)

# Train the model
model.fit(X_train, y_train)

# Predict on the validation set
print("Making predictions on the validation set...")
y_pred = model.predict(X_val)

# Calculate the accuracy
accuracy = accuracy_score(y_val, y_pred)
print(f'Validation Accuracy: {accuracy * 100:.2f}%')

# Define a directory where you want to save your models
print("Setting up model checkpoint directory...")
models_dir = 'models'
os.makedirs(models_dir, exist_ok=True)
print(f"Models will be saved in '{models_dir}' directory.")

# Save the model
print("Saving the logistic regression model...")
model_path = os.path.join(models_dir, 'logistic_regression_model.pkl')
joblib.dump(model, model_path)
print(f"Model saved successfully at '{model_path}'.")

print("Model training and evaluation complete.")
