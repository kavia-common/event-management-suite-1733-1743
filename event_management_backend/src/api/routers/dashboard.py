from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import schemas, models
from ..database import get_async_session
from .auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_model=schemas.UserDashboardOut, summary="Get user dashboard info")
async def user_dashboard(db: AsyncSession = Depends(get_async_session), current_user: models.User = Depends(get_current_user)):
    created_events_result = await db.execute(
        select(models.Event).where(models.Event.creator_id == current_user.id)
    )
    created_events = created_events_result.scalars().all()

    registered_events_result = await db.execute(
        select(models.Event)
        .join(models.Attendee, models.Event.id == models.Attendee.event_id)
        .where(models.Attendee.user_id == current_user.id)
    )
    registered_events = registered_events_result.scalars().all()

    return schemas.UserDashboardOut(created_events=created_events, registered_events=registered_events)
