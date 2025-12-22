
import os
import re
import nltk
import pandas as pd
import numpy as np
import requests
import zipfile
import io
import joblib

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def download_dataset(url, extract_to):
    print(f"Downloading dataset from {url} ...")
    response = requests.get(url)
    if response.status_code == 200:
        print("[+] Download successful!")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(extract_to)
        print("[+] Extraction completed.")
    else:
        print(f"[-] Failed to download dataset: {response.status_code}")


def preprocess_message(message, stop_words, stemmer):
    message = message.lower()
    message = re.sub(r"[^a-z\s$!]", "", message)
    tokens = word_tokenize(message)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [stemmer.stem(word) for word in tokens]
    return " ".join(tokens)

def load_and_preprocess_data(file_path):
    print("[*] Loading dataset...")
    df = pd.read_csv(file_path, sep="\t", header=None, names=["label", "message"])
    df.drop_duplicates(inplace=True)
    print(f"[+] Loaded {len(df)} messages.")

    nltk.download("punkt", quiet=True)
    nltk.download("stopwords", quiet=True)
    stop_words = set(stopwords.words("english"))
    stemmer = PorterStemmer()

    print("[*] Preprocessing text messages...")
    df["message"] = df["message"].apply(lambda x: preprocess_message(x, stop_words, stemmer))
    df["label"] = df["label"].apply(lambda x: 1 if x == "spam" else 0)

    print("[+] Preprocessing done.")
    return df

def train_model(df):
    X = df["message"]
    y = df["label"]

    vectorizer = CountVectorizer(min_df=1, max_df=0.9, ngram_range=(1, 2))
    pipeline = Pipeline([
        ("vectorizer", vectorizer),
        ("classifier", MultinomialNB())
    ])

    param_grid = {"classifier__alpha": [0.01, 0.1, 0.2, 0.5, 1.0]}
    grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring="f1")
    grid_search.fit(X, y)

    best_model = grid_search.best_estimator_
    print("[+] Best Model Parameters:", grid_search.best_params_)
    print("[+] Model training complete.")
    return best_model

def save_model(model, filename="spam_detection_model.joblib"):
    joblib.dump(model, filename)
    print(f"[+] Model saved as {filename}")

def load_model(filename="spam_detection_model.joblib"):
    return joblib.load(filename)

def predict_messages(model, messages):
    predictions = model.predict(messages)
    probabilities = model.predict_proba(messages)

    print("\n" + "="*60)
    print("📩 Prediction Results")
    print("="*60)
    for i, msg in enumerate(messages):
        prediction = "Spam" if predictions[i] == 1 else "Not-Spam"
        spam_prob = probabilities[i][1]
        ham_prob = probabilities[i][0]

        print(f"\nMessage: {msg}")
        print(f"Prediction: {prediction}")
        print(f"Spam Probability: {spam_prob:.2f}")
        print(f"Not-Spam Probability: {ham_prob:.2f}")
    print("="*60)


if __name__ == "__main__":
    # Replace with your actual HTB IP and Port
    DATASET_URL = "http://HTB-IP:8001/sms_spam_collection.zip"
    EXTRACT_PATH = "sms_spam_collection"

    download_dataset(DATASET_URL, EXTRACT_PATH)

    dataset_path = os.path.join(EXTRACT_PATH, "SMSSpamCollection")
    df = load_and_preprocess_data(dataset_path)

    model = train_model(df)
    save_model(model)

    new_messages = [
        "Congratulations! You've won a $1000 Walmart gift card. Go to http://bit.ly/1234 to claim now.",
        "Hey, are we still meeting up for lunch today?",
        "Urgent! Your account has been compromised. Verify your details here: www.fakebank.com/verify",
        "Reminder: Your appointment is scheduled for tomorrow at 10am.",
        "FREE entry in a weekly competition to win an iPad. Just text WIN to 80085 now!"
    ]

    loaded_model = load_model()
    predict_messages(loaded_model, new_messages)
