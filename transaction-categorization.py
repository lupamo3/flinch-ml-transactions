#!/usr/bin/env python3
import pandas as pd
import os
import argparse
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def load_and_preprocess_data(filepath):
    """
    Loads data from an Excel file and performs basic preprocessing.
    
    Steps:
      - Reads the Excel file.
      - Drops rows where either 'Description' or 'Category' is missing.
      - Converts the transaction descriptions to lowercase.
      - Drops duplicate records.
    
    Args:
        filepath (str): Path to the Excel file.
    
    Returns:
        DataFrame: Preprocessed data.
    """
    # Load data from Excel
    df = pd.read_excel(filepath)
    print("Initial data preview:")
    print(df.head())
    
    # Drop rows with missing 'Description' or 'Category'
    df = df.dropna(subset=['description', 'category'])
    
    # Lowercase the text in the 'Description' column
    df['description'] = df['description'].str.lower()
    
    # Remove duplicate rows if any
    df = df.drop_duplicates()
    
    return df

def vectorize_text(train_text, test_text):
    """
    Converts text data into TF-IDF vectors.
    
    Args:
        train_text (Series): Training data descriptions.
        test_text (Series): Testing data descriptions.
    
    Returns:
        X_train: TF-IDF features for training data.
        X_test: TF-IDF features for testing data.
        vectorizer: The fitted TfidfVectorizer.
    """
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train = vectorizer.fit_transform(train_text)
    X_test = vectorizer.transform(test_text)
    return X_train, X_test, vectorizer

def train_model(X_train, y_train):
    """
    Trains a Multinomial Naive Bayes classifier.
    
    Args:
        X_train: TF-IDF feature matrix for training data.
        y_train: Labels for training data.
    
    Returns:
        model: Trained classification model.
    """
    model = MultinomialNB()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluates the model performance on test data.
    
    Prints:
      - Accuracy
      - Classification report
      - Confusion matrix
    
    Args:
        model: The trained classification model.
        X_test: TF-IDF feature matrix for testing data.
        y_test: True labels for testing data.
    """
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    conf_matrix = confusion_matrix(y_test, predictions)
    
    print("Model Evaluation:")
    print("-----------------")
    print(f"Accuracy: {acc:.2f}\n")
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(conf_matrix)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Transaction Categorization Model")
    parser.add_argument('--data', type=str, default=os.path.join(os.path.dirname(__file__), "rw.xlsx"), help="Path to the Excel file containing transactions."), 
    parser.add_argument('--save_model', type=str, default=os.path.join(os.path.dirname(__file__), "transaction_model.pkl"), help="Path to save the trained model and vectorizer.")
    args = parser.parse_args()
    
    # Check if the provided data file exists
    if not os.path.exists(args.data):
        print(f"Data file does not exist: {args.data}")
        return
    
    # Load and preprocess the transaction data
    df = load_and_preprocess_data(args.data)
    
    # Use 'Description' as feature and 'Category' as the label
    X = df['description']
    y = df['category']
    
    # Split the data into training and testing sets (80% train, 20% test)
    X_train_text, X_test_text, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Convert text descriptions to numerical vectors
    X_train, X_test, vectorizer = vectorize_text(X_train_text, X_test_text)
    
    # Train the categorization model
    model = train_model(X_train, y_train)
    
    # Evaluate the model on the test set
    evaluate_model(model, X_test, y_test)
    
    # Save the trained model and vectorizer as a dictionary for later use
    joblib.dump({'model': model, 'vectorizer': vectorizer}, args.save_model)
    print(f"\nTrained model and vectorizer saved to {args.save_model}")

if __name__ == "__main__":
    main()
