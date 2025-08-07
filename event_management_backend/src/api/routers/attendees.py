from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .. import models, schemas
from ..database import get_async_session
from .auth import get_current_user

router = APIRouter(prefix="/attendees", tags=["attendees"])

@router.post("/register", response_model=schemas.AttendeeOut, summary="Register as attendee for an event")
async def register_attendee(reg: schemas.AttendeeRegister, db: AsyncSession = Depends(get_async_session), current_user: models.User = Depends(get_current_user)):
    # Check if registration already exists
    result = await db.execute(
        select(models.Attendee).where(
            models.Attendee.user_id == current_user.id,
            models.Attendee.event_id == reg.event_id
        )
    )
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Already registered for this event")
    registration = models.Attendee(user_id=current_user.id, event_id=reg.event_id)
    db.add(registration)
    await db.commit()
    await db.refresh(registration)
    return registration

@router.delete("/unregister/{event_id}", status_code=204, summary="Unregister from an event")
async def unregister_attendee(event_id: int, db: AsyncSession = Depends(get_async_session), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(
        select(models.Attendee).where(
            models.Attendee.user_id == current_user.id,
            models.Attendee.event_id == event_id
        )
    )
    registration = result.scalars().first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    await db.delete(registration)
    await db.commit()
    return

@router.get("/event/{event_id}", response_model=List[schemas.UserOut], summary="List attendees for an event")
async def list_attendees(event_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(
        select(models.User)
        .join(models.Attendee, models.User.id == models.Attendee.user_id)
        .where(models.Attendee.event_id == event_id)
    )
    return result.scalars().all()
