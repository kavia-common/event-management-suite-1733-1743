# Event Management Backend

FastAPI-based backend for the Event Management application.

## Features

- **User Authentication**: JWT-based signup/login.
- **Event CRUD**: Create, view, update, delete events.
- **User Dashboard**: List user's created and registered events.
- **Attendee Registration**: Register/unregister for events, fetch event attendees.
- **AsyncSQLAlchemy**: Fully async and scalable setup.
- **API Docs**: Interactive OpenAPI docs at `/docs`.

## Setup

1. Install requirements:
   ```
   pip install -r requirements.txt
   ```
2. Define environment variables (see `.env.example` for required vars).
3. Run the app:
   ```
   uvicorn src.api.main:app --reload
   ```

## Project Structure

- `src/api/models.py`         : SQLAlchemy ORM models
- `src/api/schemas.py`        : Pydantic request/response schemas
- `src/api/database.py`       : DB engine, session, base
- `src/api/utils.py`          : JWT and password helpers
- `src/api/config.py`         : Env + settings manager
- `src/api/routers/`          : Route modules (`auth.py`, `events.py`, etc.)
- `src/api/main.py`           : Entrypoint, router inclusion

## Endpoints Overview

- `/auth/register`      : Register (POST)
- `/auth/login`         : JWT Login (POST)
- `/auth/me`            : Self info (GET, JWT token)
- `/events/`            : List/create events (GET/POST)
- `/events/{id}`        : Read/update/delete event (GET/PUT/DELETE)
- `/attendees/register` : Register for event (POST)
- `/attendees/unregister/{event_id}` : Cancel attendance (DELETE)
- `/attendees/event/{event_id}` : List attendees (GET)
- `/dashboard/`         : Your created/registered events (GET)

## Environment Variables

See `.env.example` for configuration.

## Notes

- After first run, comment out table creation in `on_startup` and manage migrations with Alembic or similar if in production.
- Extensible project structure (add routers, models, etc. as app grows).

