from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, events, attendees, dashboard
from .database import Base, engine

app = FastAPI(
    title="Event Management Backend",
    description="API for a full-featured event management system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(attendees.router)
app.include_router(dashboard.router)

@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"message": "Healthy"}

# -----------------------------------------------------------------------------
# DB init helper (run once at launch in development to create all tables)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # Comment out this line after initial run if you manage migrations externally
        await conn.run_sync(Base.metadata.create_all)
