# -*- coding: utf-8 -*-
"""spam_msg_detector.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YGhg6di-VRMAmcoJjNWyQaqRqfoxIXEu
"""

pip install pandas scikit-learn nltk

import pandas as pd

# Load the CSV file into a DataFrame
# Try different encodings if UTF-8 fails
try:
    df = pd.read_csv('spam.csv', encoding='utf-8', usecols=['v1', 'v2'])
except UnicodeDecodeError:
    df = pd.read_csv('spam.csv', encoding='latin1', usecols=['v1', 'v2'])

# Assuming you want to read the first row of data
row_index = 0

# Extract data from v1 and v2 columns
data_v1 = df.at[row_index, 'v1']
data_v2 = df.at[row_index, 'v2']

# Printing data for demonstration
print(data_v1, "\t", data_v2)

import string
import nltk
import pandas as pd
from nltk.corpus import stopwords

# Download stopwords if not already downloaded
nltk.download('stopwords')

# Load your data into a DataFrame
# Try different encodings if UTF-8 fails
try:
    df = pd.read_csv('spam.csv', encoding='utf-8', usecols=['v1', 'v2'])
except UnicodeDecodeError:
    df = pd.read_csv('spam.csv', encoding='latin1', usecols=['v1', 'v2'])

# Define stopwords
stop_words = set(stopwords.words('english'))

# Preprocess the text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove stopwords and split into words
    words = [word for word in text.split() if word not in stop_words]
    # Join the words back into a single string
    text = ' '.join(words)
    return text

# Apply preprocessing to your text data (replace 'v2' with your actual text column name)
df['v2'] = df['v2'].apply(preprocess_text)

# Example: Print the preprocessed DataFrame
print(df.head())

from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize TF-IDF Vectorizer
tfidf = TfidfVectorizer(max_features=5000)

# Transform the text data
X = tfidf.fit_transform(df['v2']).toarray()
y = df['v1']

print(X.shape)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the models
log_reg = LogisticRegression()
naive_bayes = MultinomialNB()
svc = SVC()

# Train the models
log_reg.fit(X_train, y_train)
naive_bayes.fit(X_train, y_train)
svc.fit(X_train, y_train)

from sklearn.metrics import classification_report, accuracy_score

# Predict and evaluate
models = {'Logistic Regression': log_reg, 'Naive Bayes': naive_bayes, 'SVM': svc}
for model_name, model in models.items():
    y_pred = model.predict(X_test)
    print(f"{model_name} Accuracy: {accuracy_score(y_test, y_pred)}")
    print(classification_report(y_test, y_pred))

import joblib

# Save the best model (e.g., Logistic Regression)
joblib.dump(log_reg, 'spam_classifier.pkl')

# Load the model
model = joblib.load('spam_classifier.pkl')

# Predict with the loaded model
y_pred_loaded = model.predict(X_test)
print(f"Loaded Model Accuracy: {accuracy_score(y_test, y_pred_loaded)}")

from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier

# Further Model Evaluation
for model_name, model in models.items():
    y_pred = model.predict(X_test)
    print(f"{model_name} Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    print(f"Precision: {precision_score(y_test, y_pred, pos_label='spam')}")
    print(f"Recall: {recall_score(y_test, y_pred, pos_label='spam')}")
    print(f"F1-score: {f1_score(y_test, y_pred, pos_label='spam')}")
    print(classification_report(y_test, y_pred))

# Hyperparameter Tuning (example using RandomForestClassifier)
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20]
}

rf_classifier = RandomForestClassifier()
grid_search = GridSearchCV(estimator=rf_classifier, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

best_params = grid_search.best_params_
best_estimator = grid_search.best_estimator_

print("Best parameters:", best_params)

