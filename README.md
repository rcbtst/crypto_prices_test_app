## How to run

1. `cp .env.example .env`
2. `docker-compose up`

API docs will be available on: http://localhost:8000/docs

## Design decisions

- Project written in DDD / Onion style architecture to show some clean architecture skills
- Redis is used as Celery broker and result backend for speed and simplicity
- Celery runs only one worker process since its enough for our case
- Celery runs async tasks using event loop that is created and reused via custom task class (to use same async
  interfaces everywhere)
- Sensitive data stored in env variables and parsed using pydantic-settings (allows convenient pydantic validation)
