from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from log_parser import parse_logs
from collections import Counter

LOG_FILE = "app.log"

# Step 1: Parse logs
logs = parse_logs(LOG_FILE)

# Step 2: Prepare ML data
messages = [log["clean_message"] for log in logs if log["clean_message"]]
labels = [log["level"] for log in logs if log["clean_message"]]

print("Log level distribution:")
print(Counter(labels))

# Step 3: Vectorize text
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)
X = vectorizer.fit_transform(messages)

# Step 4: Train / test split
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.2, random_state=42, stratify=labels
)

# Step 5: Train classifier
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Step 6: Evaluate
y_pred = model.predict(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Step 7: Sample predictions
print("\nSample predictions:")
print("-" * 50)
for msg, pred in zip(messages[:10], model.predict(X[:10])):
    print(f"{msg[:70]} → {pred}")
