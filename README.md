# fastapi-workout-api
# Workout Tracker API

I built this API from scratch to get hands-on with FastAPI. I specifically turned off the aggressive AI auto-complete in VS Code while writing this so I could actually build the muscle memory for the framework instead of just letting a ghostwriter do it for me. 

Right now, it's a fully functional CRUD backend for tracking workout movements, sets, and targeted muscle groups.

## The Stack
-> FastAPI
-> Pydantic (for strict data validation)
-> Python 3.x
-> Uvicorn (for the local server)

## How It Works Under the Hood
I focused heavily on the mechanics of how data enters and leaves the API:

-> The Bouncers: I used Pydantic models to strictly validate incoming JSON. If you try to send a workout with a muscle group under 3 characters or negative sets, the API rejects it with a 422 error.
-> Proper Status Codes: I overrode the default 200 OK responses to use standard REST codes (like `201 Created` for POST and `204 No Content` for DELETE).
-> The "Trap Doors": Built custom `HTTPException` logic. If a request finishes searching the database and comes up empty (like looking up a bad ID), it hits a trap door and throws a clean `404 Not Found` instead of crashing the app silently.
-> Case-Insensitive Filtering: Added `.casefold()` logic to the GET endpoints so users can search for muscle groups without worrying about exact capitalization.
