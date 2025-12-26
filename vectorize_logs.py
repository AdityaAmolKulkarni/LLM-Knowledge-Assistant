from sklearn.feature_extraction.text import TfidfVectorizer
from log_parser import parse_logs

LOG_FILE = "app.log"

# Step 1: Parse logs (single source of truth)
logs = parse_logs(LOG_FILE)

# Step 2: Collect cleaned messages
cleaned_messages = [
    log["clean_message"] for log in logs if log["clean_message"]
]

# Step 3: Convert text to numbers
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X = vectorizer.fit_transform(cleaned_messages)

# Step 4: Inspect results (safe preview)
print("Number of logs vectorized:", X.shape[0])
print("Vocabulary size:", X.shape[1])

print("\nSample learned words:")
print(vectorizer.get_feature_names_out()[:20])

print("\nSample numeric vectors:")
print(X.toarray()[:3])
