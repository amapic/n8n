import json

import anthropic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from analyze import analyze_ticket

app = FastAPI(title="Product Ops Copilot")


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
    return {"id": ticket.id, "title": ticket.title, "analysis_json": analysis}
