from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, description="Password with minimum 6 characters")
    full_name: Optional[str] = Field(None, description="Full name")

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: int
    exp: int

# Event schemas
class EventBase(BaseModel):
    title: str
    description: Optional[str]
    location: Optional[str]
    start_time: datetime
    end_time: datetime

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class EventOut(EventBase):
    id: int
    creator_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Attendee/Registration schemas
class AttendeeRegister(BaseModel):
    event_id: int

class AttendeeOut(BaseModel):
    id: int
    user_id: int
    event_id: int
    registered_at: datetime

    class Config:
        orm_mode = True

# User Dashboard
class UserDashboardOut(BaseModel):
    created_events: List[EventOut]
    registered_events: List[EventOut]
