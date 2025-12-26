from datetime import datetime
import re

# Example log line handled:
# 2016-09-29 00:01:47, Info  CBS  Failed to get next element [HRESULT = 0x800f080d]

LOG_PATTERN = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\s*'
    r'(?P<level>\w+)\s+'
    r'(?P<component>\w+)\s+'
    r'(?P<message>.*)'
)

def parse_logs(log_file_path):
    logs = []

    with open(log_file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            match = LOG_PATTERN.match(line)
            if not match:
                # Skip lines that don't match the expected format
                continue

            try:
                timestamp = datetime.strptime(
                    match.group("timestamp"),
                    "%Y-%m-%d %H:%M:%S"
                )

                level = match.group("level")          # Info, Warning, etc.
                service = match.group("component")    # CBS, CSI, etc.
                message = match.group("message")

                # Clean message for ML
                clean_message = message.lower()
                clean_message = re.sub(r"0x[0-9a-fA-F]+", "", clean_message)  # hex codes
                clean_message = re.sub(r"\d+", "", clean_message)
                clean_message = re.sub(r"\s+", " ", clean_message).strip()

                logs.append({
                    "timestamp": timestamp,
                    "level": level,
                    "service": service,
                    "message": message,
                    "clean_message": clean_message
                })

            except Exception:
                # Defensive programming: skip bad lines safely
                continue

    return logs
