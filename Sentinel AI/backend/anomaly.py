import numpy as np
from sklearn.ensemble import IsolationForest


def detect_anomalies(df):
    numeric = df.select_dtypes(include="number").dropna(axis=1, how="all")
    if numeric.empty:
        # Fallback when no numeric columns exist
        return {"mean": {}, "std": {}, "signals": ["no numeric fields detected"], "top_features": []}, 0.0

    filled = numeric.fillna(numeric.median())

    if len(filled) >= 2:
        model = IsolationForest(contamination=0.1, random_state=42)
        model.fit(filled)
        scores = model.decision_function(filled)
        score_min, score_max = scores.min(), scores.max()
        if score_max == score_min:
            normalized_score = 0.5
        else:
            normalized_score = float(np.clip((score_max - scores.mean()) / (score_max - score_min + 1e-9), 0.0, 1.0))
    else:
        # Not enough history for the model; stay neutral.
        normalized_score = 0.5
        scores = np.array([0.0])

    means = numeric.mean()
    raw_stds = numeric.std()
    stds = raw_stds.replace(0, 1e-9)
    latest = numeric.iloc[-1]

    def build_trend_hint(series):
        window = min(5, max(2, len(series) // 2))
        if len(series) < window * 2:
            return "trend unclear"
        recent_mean = series.tail(window).mean()
        prior_mean = series.head(window).mean()
        delta = recent_mean - prior_mean
        if abs(delta) <= series.std() * 0.2:
            return "stable"
        return "increasing" if delta > 0 else "decreasing"

    z_scores = ((latest - means).abs() / (stds + 1e-9)).sort_values(ascending=False)
    top_features = []
    signals = []
    for feature in z_scores.head(3).index:
        deviation = float(round(z_scores[feature], 2))
        direction = "above" if latest[feature] >= means[feature] else "below"
        trend_hint = build_trend_hint(numeric[feature])
        detail = {
            "feature": feature,
            "deviation_sigma": deviation,
            "direction": direction,
            "trend": trend_hint
        }
        top_features.append(detail)
        signals.append(f"{feature} running {direction} baseline ({deviation}σ) with {trend_hint} trend")

    if not signals:
        signals = ["statistical deviation detected"]

    summary = {
        "mean": means.to_dict(),
        "std": raw_stds.to_dict(),
        "signals": signals,
        "top_features": top_features,
        "risk_score": normalized_score
    }
    return summary, normalized_score