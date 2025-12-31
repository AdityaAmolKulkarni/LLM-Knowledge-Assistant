import streamlit as st
import pandas as pd

from log_parser import parse_logs
from severity import infer_severity
from summarizer import incidents  # or re-run logic inline if needed

st.set_page_config(page_title="AI Log Analyzer", layout="wide")

st.title("🧠 AI-Powered Log Analysis System")
st.write("Upload a log file to analyze incidents, severity, and summaries.")

# --------------------------------------------------
# File upload
# --------------------------------------------------
uploaded_file = st.file_uploader("Upload log file", type=["log", "txt"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp.log", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Log file uploaded successfully.")

    # --------------------------------------------------
    # Parse logs
    # --------------------------------------------------
    logs = parse_logs("temp.log")

    st.subheader("Parsed Logs Preview")
    df = pd.DataFrame(logs)
    st.dataframe(df.head(20))

    # --------------------------------------------------
    # Severity Analysis
    # --------------------------------------------------
    st.subheader("Severity Classification")

    severities = []
    for log in logs:
        severity = infer_severity(log["clean_message"])
        severities.append(severity)

    df["severity"] = severities

    severity_counts = df["severity"].value_counts()

    st.bar_chart(severity_counts)

    # --------------------------------------------------
    # Incident Summary
    # --------------------------------------------------
    st.subheader("Incident Summary")

    from collections import defaultdict

    incident_map = defaultdict(list)

    for log in logs:
        key = (log["service"], log["message"])
        incident_map[key].append(log["timestamp"])

    summaries = []

    for (service, message), timestamps in incident_map.items():
        if len(timestamps) > 1:
            summaries.append({
                "service": service,
                "count": len(timestamps),
                "start_time": min(timestamps),
                "end_time": max(timestamps),
                "message": message[:100]
            })

    summary_df = pd.DataFrame(summaries)
    st.dataframe(summary_df)

    st.success("Analysis complete.")
