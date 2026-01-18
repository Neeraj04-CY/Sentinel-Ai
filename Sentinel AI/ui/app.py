import os
import sys
import io
import pandas as pd
import streamlit as st

# Ensure backend modules are importable when running from the ui folder
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from backend.pipeline import run_pipeline  # noqa: E402

st.set_page_config(page_title="SentinelAI", layout="wide")
st.title("SentinelAI Decision Console")

st.markdown(
    """
Mission-driven AI operations. Issue a mission, feed signals, and let SentinelAI decide and act.
"""
)

# Example templates for quick demos
example_small = pd.DataFrame({
    "volume": [100, 110, 105, 220, 240],
    "latency_ms": [120, 118, 125, 210, 230],
    "errors": [2, 1, 2, 6, 7]
})

example_multi = pd.DataFrame({
    "txn_amount": [500, 520, 510, 980, 1020],
    "txn_count": [50, 48, 52, 130, 140],
    "chargebacks": [1, 1, 1, 4, 5],
    "geo_variance": [0.1, 0.12, 0.11, 0.32, 0.35]
})

col_a, col_b = st.columns(2)
with col_a:
    buf = io.StringIO()
    example_small.to_csv(buf, index=False)
    st.download_button("Download Template: Ops Spike", data=buf.getvalue(), file_name="sentinel_ops_spike.csv", mime="text/csv")
with col_b:
    buf = io.StringIO()
    example_multi.to_csv(buf, index=False)
    st.download_button("Download Template: Fraud Burst", data=buf.getvalue(), file_name="sentinel_fraud_burst.csv", mime="text/csv")

st.divider()

st.subheader("Mission Brief")
mission_input = st.text_area(
    "Describe the operational goal.",
    value="Safeguard critical transactions and prevent fraudulent bursts.",
    height=80,
)

st.subheader("Upload Signals (CSV)")
uploaded = st.file_uploader("Upload telemetry or event CSV", type=["csv"])

if "last_output" not in st.session_state:
    st.session_state.last_output = None
if "selected_command" not in st.session_state:
    st.session_state.selected_command = None
if "command_log" not in st.session_state:
    st.session_state.command_log = []


def render_decision(output):
    st.subheader("Mission Status")
    status = output.get("mission_status", "COMPLETED")
    st.success(status)

    st.subheader("SentinelAI Intelligence")
    st.info(output.get("system_summary", "SentinelAI processed the mission and issued a decision."))

    risk_color = {"HIGH": "#d64550", "MEDIUM": "#f4a261", "LOW": "#2a9d8f"}
    risk = output.get("risk_level", "MEDIUM")
    color = risk_color.get(risk, "#2a9d8f")

    st.subheader("Risk Level")
    st.markdown(f"""
    <div style='padding:12px;border:1px solid #e5e7eb;border-radius:10px;'>
      <span style='background:{color};color:white;padding:12px 16px;border-radius:10px;font-weight:800;font-size:18px;'>{risk}</span>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Key Signals")
    signals = output.get("signals", []) or ["No signals available"]
    for sig in signals:
        st.markdown(f"- {sig}")

    st.subheader("System Analysis")
    st.write(output.get("analysis", "No analysis generated."))

    st.subheader("Primary Recommended Action")
    st.success(output.get("recommended_action", "No action generated."))

    with st.expander("How SentinelAI Reasoned", expanded=False):
        trace = output.get("decision_flow") or output.get("reasoning_trace") or []
        if trace:
            for step in trace:
                st.markdown(f"- {step}")
        else:
            st.markdown(f"- {output.get('analysis', 'No reasoning available.')}")

    st.subheader("Command Options")
    options_detail = output.get("command_options_detail") or []
    options_strings = output.get("command_options") or []
    if options_detail:
        labels = [opt.get("label", opt.get("action", "Option")) for opt in options_detail]
        selection = st.radio("Select a command to execute", labels, index=0, key="selected_command")
        chosen = next((opt for opt in options_detail if opt.get("label") == selection), options_detail[0])
        st.success(f"{chosen.get('action', '')} — {chosen.get('note', '')}")
        if st.button("Confirm Command Execution"):
            st.session_state.command_log.append(f"Executed: {chosen.get('action', '')}")
    elif options_strings:
        selection = st.radio("Select a command to execute", options_strings, index=0, key="selected_command")
        st.success(selection)
        if st.button("Confirm Command Execution"):
            st.session_state.command_log.append(f"Executed: {selection}")
    else:
        st.info(output.get("recommended_action", "No action generated."))

    st.subheader("Execution Log")
    log_entries = (output.get("execution_log") or []) + (st.session_state.command_log or [])
    for entry in log_entries:
        st.markdown(f"- {entry}")


if st.button("Execute Mission"):
    if uploaded is None:
        st.error("Upload a CSV first to brief SentinelAI.")
    else:
        try:
            df = pd.read_csv(uploaded)
            output = run_pipeline(df, mission=mission_input)
            st.session_state.last_output = output
        except Exception as exc:
            st.error(f"Failed to process file: {exc}")

if st.session_state.last_output:
    render_decision(st.session_state.last_output)
else:
    st.info("Upload a CSV, brief the mission, and execute to see SentinelAI's command interface. Use the templates above for a fast demo.")
