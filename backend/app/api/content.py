from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class ContentCreate(BaseModel):
    title: str
    body: str
    content_type: str = "article"


class ContentResponse(BaseModel):
    id: str
    title: str
    body: str
    content_type: str
    categories: List[str] = []
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime


# In-memory store (replace with database in production)
_store: List[dict] = []
_counter = 0


@router.get("/", response_model=List[ContentResponse])
async def list_content(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    content_type: Optional[str] = None
):
    items = [
        i for i in _store if not content_type or i["content_type"] == content_type]
    start = (page - 1) * limit
    return items[start:start + limit]


@router.post("/", response_model=ContentResponse, status_code=201)
async def create_content(data: ContentCreate):
    global _counter
    _counter += 1
    now = datetime.utcnow()
    item = {
        "id": str(_counter),
        "title": data.title,
        "body": data.body,
        "content_type": data.content_type,
        "categories": [],
        "tags": [],
        "created_at": now,
        "updated_at": now
    }
    _store.append(item)
    return item


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(content_id: str):
    for item in _store:
        if item["id"] == content_id:
            return item
    raise HTTPException(status_code=404, detail="Content not found")


@router.delete("/{content_id}")
async def delete_content(content_id: str):
    global _store
    _store = [i for i in _store if i["id"] != content_id]
    return {"message": "Deleted"}
