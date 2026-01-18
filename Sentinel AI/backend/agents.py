LEVELS = ["LOW", "MEDIUM", "HIGH"]
LEVEL_INDEX = {level: idx for idx, level in enumerate(LEVELS)}


def _severity_from_features(features):
    if not features:
        return "LOW"
    max_dev = max(f.get("deviation_sigma", 0.0) for f in features)
    if max_dev >= 2.5 or len(features) >= 3:
        return "HIGH"
    if max_dev >= 1.5 or len(features) >= 2:
        return "MEDIUM"
    return "LOW"


def analyst_agent(summary):
    top_features = summary.get("top_features") or []
    signals = summary.get("signals") or []

    severity = _severity_from_features(top_features)
    if top_features:
        primary = top_features[0]
        secondary = ", ".join(f"{f['feature']} ({f['direction']})" for f in top_features[1:3])
        message = (
            f"Situation: {primary['feature']} running {primary['direction']} norms"
            f" ({primary['deviation_sigma']}σ) with {primary['trend']} momentum."
        )
        if secondary:
            message += f" Secondary pressure on {secondary}."
    elif signals:
        message = signals[0]
    else:
        message = "No numeric metrics available for analysis."

    return {
        "summary": message,
        "severity_hint": severity,
        "focus_feature": top_features[0].get("feature") if top_features else None
    }


def _level_from_score(score):
    if score >= 0.67:
        return "HIGH"
    if score >= 0.33:
        return "MEDIUM"
    return "LOW"


def risk_agent(analyst_report, score):
    score_level = _level_from_score(score)
    analyst_level = analyst_report.get("severity_hint", "LOW")
    score_idx = LEVEL_INDEX.get(score_level, 0)
    analyst_idx = LEVEL_INDEX.get(analyst_level, 0)
    gap = abs(score_idx - analyst_idx)

    if gap == 0:
        chosen = score_level
        note = "Risk score corroborates analyst narrative."
        modifier = 1.0
    else:
        chosen = LEVELS[max(score_idx, analyst_idx)]
        modifier = 0.85 if gap == 1 else 0.75
        if score_idx > analyst_idx:
            note = "Score indicates higher risk than analyst summary; conservative stance applied."
        else:
            note = "Analyst highlighted greater pressure than score; hedging with uncertainty."

    return chosen, note, modifier


def _pattern_from_features(top_features):
    if not top_features:
        return "default", "Signals stable; precautionary oversight recommended."

    primary = top_features[0]
    direction = primary.get("direction")
    trend = primary.get("trend")
    feature = primary.get("feature")

    if direction == "above" and trend == "increasing":
        return "surge", f"{feature} is accelerating upward."
    if direction == "below" and trend == "decreasing":
        return "drop", f"{feature} is sliding below safe bounds."
    if len(top_features) > 1:
        return "broad", "Multiple metrics are moving together."
    return "default", f"{feature} is unstable versus baseline."


def action_agent(risk_level, summary):
    top_features = summary.get("top_features") or []
    pattern, pattern_reason = _pattern_from_features(top_features)

    actions = {
        "HIGH": {
            "surge": (
                "Freeze affected flows and escalate to incident lead",
                0.9,
                "Rapid upward pressure warrants an immediate halt."
            ),
            "drop": (
                "Pause payouts, validate data feeds, and alert finance oversight",
                0.88,
                "Sharp drop could signal tampering or outages."
            ),
            "broad": (
                "Lock down impacted services and convene crisis bridge",
                0.89,
                "Coordinated anomalies require cross-team response."
            ),
            "default": (
                "Enforce manual approval on all risky operations",
                0.87,
                "General instability detected at high risk."
            )
        },
        "MEDIUM": {
            "surge": (
                "Rate-limit transactions and queue secondary screening",
                0.75,
                "Upward drift manageable with throttling."
            ),
            "drop": (
                "Hold low-signal workloads and request operator check",
                0.73,
                "Falling metric needs verification before resuming."
            ),
            "broad": (
                "Schedule rapid review with ops and tighten monitoring thresholds",
                0.74,
                "Multiple pressure points need coordinated scrutiny."
            ),
            "default": (
                "Keep workflows running with elevated watch",
                0.72,
                "Moderate anomaly without clear pattern."
            )
        },
        "LOW": {
            "surge": (
                "Apply soft caps and re-check in next cycle",
                0.6,
                "Minor uptick observed; gentle dampening is enough."
            ),
            "drop": (
                "Log deviation and verify sensors during routine checks",
                0.58,
                "Small dip likely noise but worth logging."
            ),
            "broad": (
                "Document pattern and expand automated watchlist",
                0.59,
                "Light multi-signal variance detected."
            ),
            "default": (
                "Continue operations with automated monitoring",
                0.55,
                "No acute pressure despite anomaly flag."
            )
        }
    }

    command_sets = {
        "HIGH": [
            "Escalate to incident command and freeze flows",
            "Quarantine affected services and require manual overrides",
            "Route transactions through safe path with human approval"
        ],
        "MEDIUM": [
            "Throttle high-risk operations and schedule rapid review",
            "Enable enhanced monitoring for flagged segments",
            "Run secondary verification on suspect batches"
        ],
        "LOW": [
            "Continue with monitoring enabled",
            "Log deviation and re-evaluate next cycle",
            "Notify ops lead of minor variance"
        ]
    }

    action_text, base_conf, rationale = actions[risk_level].get(pattern, actions[risk_level]["default"])
    reason = f"{pattern_reason} {rationale}".strip()
    return action_text, base_conf, reason, command_sets[risk_level]