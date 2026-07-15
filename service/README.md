# Incident Commander Demo Service

Synthetic FastAPI service monitored by the Incident Commander hackathon agent. It intentionally has a small commit history that can be used to demonstrate diagnosis and draft-only remediation PRs. No production data or credentials are used.

Run locally:

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload
```
