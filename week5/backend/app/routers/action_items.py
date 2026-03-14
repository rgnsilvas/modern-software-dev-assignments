from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import ActionItemCreate, ActionItemRead, PaginatedActionItemResponse

router = APIRouter(prefix="/action-items", tags=["action_items"])


@router.get("/", response_model=PaginatedActionItemResponse)
def list_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PaginatedActionItemResponse:
    total = db.execute(select(func.count(ActionItem.id))).scalar()
    offset = (page - 1) * page_size
    rows = db.execute(select(ActionItem).offset(offset).limit(page_size)).scalars().all()
    items = [ActionItemRead.model_validate(row) for row in rows]
    return PaginatedActionItemResponse(items=items, total=total)


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)
