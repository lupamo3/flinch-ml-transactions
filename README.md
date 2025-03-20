# README / Explanation

## Overview
This code is designed to demonstrate a simple machine learning pipeline for transaction categorization. To showcase the ability to work with data and apply fundamental machine learning concepts.

---

## Key Steps

### Data Loading and Preprocessing
1. The script reads the transaction data from an Excel file using `pandas.read_excel()`.
2. Rows with missing values in the `Description` or `Category` columns are dropped.
3. Text in the `Description` column is converted to lowercase for uniformity.

### Vectorization
1. The `TfidfVectorizer` is used to convert transaction descriptions (text data) into numerical feature vectors.

### Model Training
1. A `Multinomial Naive Bayes` classifier is employed due to its simplicity and effectiveness for text classification.

### Evaluation
1. The model’s performance is assessed using common metrics:
   - **Accuracy**
   - **Classification Report**: i.e precision, recall, and F1 scores.
   - **Confusion Matrix**

### Saving the Model
1. The trained model and vectorizer are saved to disk using `joblib`.

---

## Notes
- Future improvements may include:
  - Using alternative classifiers (e.g., Logistic Regression, Random Forest)
