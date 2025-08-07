from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .. import models, schemas
from ..database import get_async_session
from .auth import get_current_user

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=schemas.EventOut, summary="Create an event")
async def create_event(event_in: schemas.EventCreate, db: AsyncSession = Depends(get_async_session), current_user: models.User = Depends(get_current_user)):
    event = models.Event(**event_in.dict(), creator_id=current_user.id)
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event

@router.get("/", response_model=List[schemas.EventOut], summary="List all events")
async def list_events(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(models.Event))
    return result.scalars().all()

@router.get("/{event_id}", response_model=schemas.EventOut, summary="Get event details by ID")
async def get_event(event_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(models.Event).where(models.Event.id == event_id))
    event = result.scalars().first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=schemas.EventOut, summary="Update an event")
async def update_event(event_id: int, event_in: schemas.EventUpdate, db: AsyncSession = Depends(get_async_session), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Event).where(models.Event.id == event_id))
    event = result.scalars().first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
    for attr, value in event_in.dict(exclude_unset=True).items():
        setattr(event, attr, value)
    await db.commit()
    await db.refresh(event)
    return event

@router.delete("/{event_id}", status_code=204, summary="Delete an event")
async def delete_event(event_id: int, db: AsyncSession = Depends(get_async_session), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Event).where(models.Event.id == event_id))
    event = result.scalars().first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    await db.delete(event)
    await db.commit()
    return
