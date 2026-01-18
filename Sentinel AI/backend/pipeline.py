from .anomaly import detect_anomalies
from .agents import analyst_agent, risk_agent, action_agent

SAFE_FALLBACK = {
    "risk_level": "MEDIUM",
    "signals": ["Automated safeguard engaged"],
    "analysis": "System could not complete reasoning path. Manual review required.",
    "recommended_action": "Manual review required",
    "confidence": 0.6,
    "system_summary": "SentinelAI defaulted to a safe manual review due to incomplete reasoning.",
    "reasoning_trace": ["Fallback engaged: manual review required."],
    "mission_brief": "Mission not provided; defaulting to protection mode.",
    "decision_flow": [
        "Mission: default protection",
        "Intelligence: unavailable",
        "Decision: hold",
        "Action: manual review"
    ],
    "command_options": [
        "Manual review required",
        "Hold operations, increase sampling",
        "Escalate to duty officer"
    ],
    "command_options_detail": [
        {
            "label": "Manual review",
            "action": "Manual review required",
            "note": "Safe default while intel is incomplete.",
            "recommended": True
        }
    ],
    "execution_log": ["Decision deferred pending manual review."],
    "mission_status": "DEFERRED"
}


def _apply_confidence(base, modifier):
    adjusted = round(base * modifier, 2)
    if adjusted <= 0:
        return 0.6
    if adjusted >= 1:
        return 0.99
    return adjusted


def run_pipeline(df, mission: str | None = None):
    summary = {}
    mission_brief = mission.strip() if mission else "Protect the current operation."
    try:
        summary, anomaly_score = detect_anomalies(df)
    except Exception:
        return SAFE_FALLBACK.copy()

    try:
        analyst_report = analyst_agent(summary)
        if not analyst_report or not analyst_report.get("summary"):
            raise ValueError("Analyst agent returned empty output")

        risk_level, risk_note, confidence_modifier = risk_agent(analyst_report, anomaly_score)
        action, base_confidence, action_reason, command_options = action_agent(risk_level, summary)
        if not action:
            raise ValueError("Action agent returned empty action")

        analysis_trace = [
            f"Analyst: {analyst_report['summary']}",
            f"Risk check: {risk_note}",
            f"Action rationale: {action_reason}"
        ]
        analysis_text = ". ".join(analysis_trace[:3])

        system_summary = f"SentinelAI assessed {risk_level} risk for the mission and advises: {action}."

        decision_flow = [
            f"Mission: {mission_brief}",
            f"Intelligence: {analyst_report['summary']}",
            f"Decision: {risk_level} with {risk_note}",
            f"Action: {action}"
        ]

        execution_log = [
            f"Mission received: {mission_brief}",
            f"Intel compiled: {analyst_report['summary']}",
            f"Decision framed: {risk_level}",
            f"Action proposed: {action}"
        ]

        command_options_detail = [
            {
                "label": "Execute recommended",
                "action": action,
                "note": action_reason,
                "recommended": True
            }
        ]
        for opt in command_options:
            if opt == action:
                continue
            command_options_detail.append({
                "label": opt,
                "action": opt,
                "note": "Alternative command option",
                "recommended": False
            })

        return {
            "risk_level": risk_level,
            "signals": (summary.get("signals", []) or [])[:4],
            "analysis": analysis_text,
            "recommended_action": action,
            "confidence": _apply_confidence(base_confidence, confidence_modifier),
            "system_summary": system_summary,
            "reasoning_trace": analysis_trace,
            "mission_brief": mission_brief,
            "decision_flow": decision_flow,
            "command_options": command_options,
            "command_options_detail": command_options_detail,
            "execution_log": execution_log,
            "mission_status": "COMPLETED"
        }
    except Exception:
        fallback = SAFE_FALLBACK.copy()
        fallback["signals"] = summary.get("signals", SAFE_FALLBACK["signals"])
        return fallback