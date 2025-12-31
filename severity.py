from collections import defaultdict
from log_parser import parse_logs

# --------------------------------------------------
# Severity keywords
# --------------------------------------------------
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


# --------------------------------------------------
# Base severity inference
# --------------------------------------------------
def infer_severity(clean_message: str) -> str:
    """
    Infer base severity from message content.
    """
    msg = clean_message.lower()

    for word in HIGH_SEVERITY_KEYWORDS:
        if word in msg:
            return "HIGH"

    for word in MEDIUM_SEVERITY_KEYWORDS:
        if word in msg:
            return "MEDIUM"

    return "LOW"


# --------------------------------------------------
# Frequency-based escalation
# --------------------------------------------------
def build_incident_index(logs):
    """
    Build incident frequency index.
    """
    incident_counts = defaultdict(list)

    for log in logs:
        key = (log["service"], log["clean_message"])
        incident_counts[key].append(log["timestamp"])

    return incident_counts


def frequency_boost(service, clean_message, incident_index):
    """
    Escalate severity based on repetition frequency.
    """
    count = len(incident_index.get((service, clean_message), []))

    if count >= 5:
        return "CRITICAL"
    elif count >= 3:
        return "HIGH"

    return None


# --------------------------------------------------
# Script mode (only runs if called directly)
# --------------------------------------------------
if __name__ == "__main__":
    LOG_FILE = "app.log"

    logs = parse_logs(LOG_FILE)
    incident_index = build_incident_index(logs)

    print("\nLOG SEVERITY OUTPUT")
    print("-" * 70)

    for log in logs[:50]:  # preview only
        base_severity = infer_severity(log["clean_message"])
        boost = frequency_boost(
            log["service"],
            log["clean_message"],
            incident_index
        )

        final_severity = boost if boost else base_severity

        print(
            f"{log['timestamp']} | "
            f"{log['service']} | "
            f"{final_severity} | "
            f"{log['message'][:80]}"
        )
