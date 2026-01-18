# SentinelAI — Minimal MVP

## Run backend
```bash
uvicorn backend.main:app --reload
```

## Run UI
```bash
streamlit run ui/app.py
```

## API
`POST /analyze` with multipart CSV file.

## Output contract
```json
{
  "risk_level": "HIGH",
  "signals": ["spike in volume", "deviation from baseline"],
  "analysis": "Transaction frequency increased 4x compared to historical mean.",
  "recommended_action": "Flag and require manual review",
  "confidence": 0.87
}
```