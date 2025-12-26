from collections import defaultdict
from log_parser import parse_logs

LOG_FILE = "app.log"

logs = parse_logs(LOG_FILE)

# Keywords that indicate actual incidents
INCIDENT_KEYWORDS = [
    "failed",
    "error",
    "exception",
    "cannot",
    "could not",
    "corrupt",
    "timeout",
    "hresult"
]

# Group incidents by (service, clean_message)
incidents = defaultdict(list)

for log in logs:
    clean_msg = log["clean_message"]

    if not clean_msg:
        continue

    # Detect incident semantically (not via log level)
    if any(word in clean_msg for word in INCIDENT_KEYWORDS):
        key = (log["service"], clean_msg)
        incidents[key].append(log["timestamp"])

# Generate summaries
print("\nINCIDENT SUMMARY")
print("-" * 70)

for (service, clean_message), timestamps in incidents.items():
    count = len(timestamps)
    start_time = min(timestamps)
    end_time = max(timestamps)

    if count == 1:
        summary = (
            f"Single incident in {service} at {start_time}: "
            f"{clean_message}"
        )
    else:
        summary = (
            f"{count} occurrences in {service} between "
            f"{start_time} and {end_time}: {clean_message}"
        )

    print(summary)
