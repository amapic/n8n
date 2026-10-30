import json
import os
import anthropic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from analyze import analyze_ticket

app = FastAPI(title="Product Ops Copilot")

def _get_model_name():
    AI_PROVIDER = os.getenv("AI_PROVIDER")
    if AI_PROVIDER == "copilot":
        return os.getenv("COPILOT_MODEL") or "auto"
    return os.getenv("CLAUDE_MODEL")

class Ticket(BaseModel):
    id: str = ""
    title: str = ""
    description: str = ""
    labels: str = ""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(ticket: Ticket):
   
    try:
        analysis = analyze_ticket(ticket.model_dump())
    except anthropic.APIError as exc:
        raise HTTPException(status_code=502, detail=f"Erreur API Anthropic : {exc}")
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=422, detail=f"Réponse du modèle invalide : {exc}")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Erreur fournisseur IA : {type(exc).__name__}: {exc}")
    return {"id": ticket.id, "title": ticket.title, "model": _get_model_name(), "analysis_json": analysis}
