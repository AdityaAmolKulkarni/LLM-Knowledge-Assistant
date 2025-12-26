from collections import defaultdict
from log_parser import parse_logs

LOG_FILE = "app.log"

logs = parse_logs(LOG_FILE)

# Keywords that indicate real problems
HIGH_SEVERITY_KEYWORDS = [
    "failed",
    "error",
    "invalid",
    "corrupt",
    "cannot",
    "could not",
    "exception",
    "hresult",
    "e_fail"
]

MEDIUM_SEVERITY_KEYWORDS = [
    "warning",
    "retry",
    "timeout",
    "unrecognized"
]

# Group logs by (service, clean_message) for frequency analysis
incident_counts = defaultdict(list)

for log in logs:
    key = (log["service"], log["clean_message"])
    incident_counts[key].append(log["timestamp"])


def infer_severity_from_text(clean_message: str) -> str:
    """
    Infer base severity from message content.
    """
    for word in HIGH_SEVERITY_KEYWORDS:
        if word in clean_message:
            return "HIGH"

    for word in MEDIUM_SEVERITY_KEYWORDS:
        if word in clean_message:
            return "MEDIUM"

    return "LOW"


def frequency_boost(service, clean_message):
    """
    Escalate severity based on repetition frequency.
    """
    count = len(incident_counts[(service, clean_message)])

    if count >= 5:
        return "CRITICAL"
    elif count >= 3:
        return "HIGH"

    return None


# Final severity assignment (preview)
print("\nLOG SEVERITY OUTPUT")
print("-" * 70)

for log in logs[:50]:  # preview only
    base_severity = infer_severity_from_text(log["clean_message"])
    boost = frequency_boost(log["service"], log["clean_message"])

    final_severity = boost if boost else base_severity

    print(
        f"{log['timestamp']} | "
        f"{log['service']} | "
        f"{final_severity} | "
        f"{log['message'][:80]}"
    )
