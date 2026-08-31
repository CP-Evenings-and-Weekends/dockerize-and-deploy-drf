# DRF Wine API

A pre-built Django REST Framework project used as the running example throughout **Module 5 Django** — starting with Dockerization in Week 13 Day 4, then CRUD in Week 14, auth in Week 14 Day 3, CORS and frontend integration in Week 14 Day 4, and Docker Compose / AWS deploy in Week 15 Day 4.

The API exposes a single resource — `Wine`, with `wine_name`, `price`, `varietal`, and `description`.  It's intentionally small so the focus stays on the **operational** side of the stack (Docker, Compose, auth, CORS, deployment) rather than business logic.

## Setup

Clone the branch that matches whichever lesson you're on (see **Branches** below).  Then:

```bash
git clone -b <branch-name> https://github.com/CP-Evenings-and-Weekends/drf-wine-api.git
cd drf-wine-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://localhost:8000/`.

To seed sample wines from the Django shell:

```bash
python manage.py shell
>>> exec(open("./setup_data.py").read())
```

## Branches

The repo uses branches to **snapshot the project at each stage** of the curriculum.  Check out the branch that matches the lesson you're working on:

| Branch | Stage | Used by |
|---|---|---|
| `main` | Plain DRF, no Docker, no auth | Module 5 Week 13 Day 4 starting point |
| `composeV2Start` | Project just before adding Docker Compose | Module 5 Week 15 Day 4 |
| `composeV2End` | Project after wiring up multi-service Compose | Module 5 Week 15 Day 4 |
| `withAuth` | Token authentication added | Module 5 Week 14 Day 3 |
| `withAuthCompose` | Auth + Docker Compose together | Module 5 Week 14 / 15 |
| `withCorsMiddleware` | CORS middleware configured for frontend integration | Module 5 Week 14 Day 4 |
| `nginx-improved` | nginx reverse proxy in front of DRF | Module 5 Week 15 Day 4 / deploy |

Each branch is meant to be a **clean starting point**, not the answer to the lesson — students apply the day's changes on top.

## Project structure

```
wines/             # Django project settings (settings.py, urls.py, wsgi.py)
wine_api/          # The single Django app (models, views, serializers)
manage.py
requirements.txt
setup_data.py      # Sample wines, run via `exec(open("./setup_data.py").read())` in the Django shell
docker-compose.yml # Present on Compose-related branches
```

## See also

- [Module 5 Week 13 Day 4](https://github.com/CP-Evenings-and-Weekends/curriculum/blob/main/Module_05_Django/week13/day4/README.md) — Dockerize the API
- [Module 5 Week 14 Day 3](https://github.com/CP-Evenings-and-Weekends/curriculum/blob/main/Module_05_Django/week14/day3/README.md) — Token auth
- [Module 5 Week 14 Day 4](https://github.com/CP-Evenings-and-Weekends/curriculum/blob/main/Module_05_Django/week14/day4/README.md) — CORS + frontend integration
- [Module 5 Week 15 Day 4](https://github.com/CP-Evenings-and-Weekends/curriculum/blob/main/Module_05_Django/week15/day4/README.md) — Docker Compose + AWS deploy
