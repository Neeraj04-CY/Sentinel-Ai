import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

DATA_DIR = Path(__file__).resolve().parent


def _bounded_normal(mean, std, size, low=None, high=None):
    vals = np.random.normal(mean, std, size)
    if low is not None:
        vals = np.maximum(vals, low)
    if high is not None:
        vals = np.minimum(vals, high)
    return vals


def generate_normal_ops(rows: int = 200) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "transaction_amount": _bounded_normal(500, 20, rows, low=400, high=600),
            "transaction_frequency": _bounded_normal(50, 5, rows, low=35, high=65),
            "error_rate": _bounded_normal(0.5, 0.1, rows, low=0.1, high=1.5),
            "latency_ms": _bounded_normal(120, 10, rows, low=90, high=150),
        }
    )


def generate_medium_risk_ops(rows: int = 200) -> pd.DataFrame:
    base = generate_normal_ops(rows)
    # Introduce mild drift and occasional spikes
    drift = np.linspace(0, 40, rows)
    base["transaction_amount"] += drift * 0.5
    base["transaction_frequency"] += np.sin(np.linspace(0, 3 * np.pi, rows)) * 5
    spike_indices = np.random.choice(rows, size=max(3, rows // 20), replace=False)
    base.loc[spike_indices, "error_rate"] += np.random.uniform(1.0, 2.0, size=len(spike_indices))
    base.loc[spike_indices, "latency_ms"] += np.random.uniform(30, 60, size=len(spike_indices))
    return base


def generate_high_risk_ops(rows: int = 200) -> pd.DataFrame:
    base = generate_normal_ops(rows)
    # Large upward pressure, heavy spikes, and volatility
    drift = np.linspace(0, 200, rows)
    noise = np.random.normal(0, 50, rows)
    base["transaction_amount"] += drift + noise
    base["transaction_frequency"] += np.random.normal(0, 15, rows)
    base["error_rate"] += np.random.uniform(2.0, 4.0, size=rows)
    base["latency_ms"] += np.random.uniform(60, 140, size=rows)
    # Insert extreme anomalies
    extreme_indices = np.random.choice(rows, size=max(5, rows // 15), replace=False)
    base.loc[extreme_indices, "transaction_amount"] += np.random.uniform(400, 800, size=len(extreme_indices))
    base.loc[extreme_indices, "error_rate"] += np.random.uniform(3.0, 6.0, size=len(extreme_indices))
    base.loc[extreme_indices, "latency_ms"] += np.random.uniform(120, 200, size=len(extreme_indices))
    return base


def _save(df: pd.DataFrame, name: str):
    path = DATA_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    return path


def main():
    normal = generate_normal_ops()
    medium = generate_medium_risk_ops()
    high = generate_high_risk_ops()

    n_path = _save(normal, "normal")
    m_path = _save(medium, "medium")
    h_path = _save(high, "high")

    print("Saved:")
    for p in [n_path, m_path, h_path]:
        print(f" - {p}")


if __name__ == "__main__":
    main()
