from __future__ import annotations
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel # Pydantic untuk API Contract (Refactor)
from .. import db
from ..services.extract import extract_action_items, extract_action_items_llm

router = APIRouter(prefix="/action-items", tags=["action-items"])

# TODO 3: Refactor menggunakan Pydantic untuk mendefinisikan skema data yang jelas
class ExtractRequest(BaseModel):
    text: str
    save_note: bool = False

class ActionItemResponse(BaseModel):
    id: int
    text: str

class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: List[ActionItemResponse]

@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest):
    """Endpoint manual dengan skema yang sudah dirapikan."""
    note_id = db.insert_note(payload.text) if payload.save_note else None
    items = extract_action_items(payload.text)
    ids = db.insert_action_items(items, note_id=note_id)
    return {"note_id": note_id, "items": [{"id": i, "text": t} for i, t in zip(ids, items)]}

@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(payload: ExtractRequest):
    """TODO 1, 3, & 4: Endpoint AI dengan penanganan error yang lebih baik."""
    try:
        note_id = db.insert_note(payload.text) if payload.save_note else None
        items = extract_action_items_llm(payload.text)
        ids = db.insert_action_items(items, note_id=note_id)
        return {"note_id": note_id, "items": [{"id": i, "text": t} for i, t in zip(ids, items)]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Extraction failed: {str(e)}")