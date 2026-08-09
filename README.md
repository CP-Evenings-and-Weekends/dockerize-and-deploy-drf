# Dockerize and Deploy a DRF API

Apply today's lesson to a DRF app of your choice, then deploy it on AWS using the steps from the [Deploying to AWS with Docker](https://github.com/CP-Evenings-and-Weekends/curriculum/blob/main/Module_04_Fullstack/week11/day4/README.md) lesson.

By the end you'll have:
1. A DRF app running locally as two containers (Django + Postgres) via `docker compose`
2. The same image pushed to Docker Hub
3. The whole stack running on an EC2 instance, reachable on the public web

## Pick a DRF app

Any one of these will do — pick what sounds most fun:
- Your own **School API** repo from week 12 (already has the models you built)
- The lesson's [drf-wine-api](https://github.com/CP-Evenings-and-Weekends/drf-wine-api) (smallest, fastest to deploy)
- The [Article Publications](https://github.com/CP-Evenings-and-Weekends/article-publications) project, if you've built it (it's assigned in week 15)
- Anything else with Django + DRF + a Postgres dependency

The included `Dockerfile`, `docker-compose.yml`, `run_compose.sh`, and `stop_compose.sh` are starter templates with the parts you should change marked `# CHANGE ME`.

## Requirements

### 1. Get the app running locally as two containers

- Drop the included `Dockerfile` into your chosen app's root and tweak the entrypoint (`CMD`) to match its WSGI module (e.g. `wines.wsgi:application` or `school_proj.wsgi:application`)
- Drop in the included `docker-compose.yml` and update `POSTGRES_DB` + the Django settings `NAME` to match
- Update `settings.py`:
  - `DATABASES['default']['HOST'] = 'db'` (the service name from `docker-compose.yml`)
  - `DATABASES['default']['PORT'] = 5432`
  - `ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']` so the browser request's `Host` header matches
- Use the included `run_compose.sh` to bring everything up and run migrations:
  ```bash
  chmod +x run_compose.sh stop_compose.sh
  ./run_compose.sh
  ```
- Hit one of your endpoints with `curl` or Postman.  Confirm you get JSON back.

> **Heads up**: the starter script runs migrations with `docker compose exec api ...`, same as the lesson.  `compose exec` targets the **service** name from `docker-compose.yml`, so it works no matter what your project directory (and therefore container name) happens to be — never hardcode a full container name like `drf-wine-api-api-1`.

### 2. Push the image to Docker Hub

```bash
docker login
docker tag <local_image_name> <YOUR_DOCKERHUB_USERNAME>/<app-name>
docker push <YOUR_DOCKERHUB_USERNAME>/<app-name>
```

### 3. Deploy to AWS

Follow the [Deploying to AWS with Docker](https://github.com/CP-Evenings-and-Weekends/curriculum/blob/main/Module_04_Fullstack/week11/day4/README.md) lesson:

1. Launch an EC2 instance (Amazon Linux 2023, t2.micro free tier)
2. `chmod 400 <KEYNAME>.pem` (don't skip this — SSH refuses world-readable keys)
3. SSH in, install Docker + git, clone your app repo
4. `./run_compose.sh` (or run `docker compose up -d --build` manually)
5. Open port 8000 on the security group (or use port 80 with nginx — see Stretch)
6. Visit `http://<EC2_PUBLIC_IPV4>:8000/<your-endpoint>/` in your browser

### 4. Verify

- Hit your endpoint from your local machine via the EC2 public IP
- `docker compose logs api` on the EC2 should show your requests landing
- Stop and restart the containers — your data should persist (that's what the `postgres_data` volume is for)

## Things to think about
- The lesson's Dockerfile uses `python:3.12-slim`, which works because the wine API pins `psycopg2-binary` — it installs from a prebuilt wheel.  The starter Dockerfile here uses `python:3.13-bookworm`, a fuller image that ships the build tools and `libpq` headers needed to compile plain `psycopg2` from source, in case the app you picked pins that instead.  What does each choice buy you, and when would you insist on one over the other?
- `sleep 5` before running migrations is fragile.  What's a more robust way to wait for Postgres to be ready?  (Hint: healthchecks + `depends_on: condition: service_healthy`.)
- `ALLOWED_HOSTS = ['*']` works for local dev but is risky in production.  Why?  How does the host-header check protect you?
- Your DB password is in `docker-compose.yml` right now.  What's the standard way to keep secrets out of source control on AWS?  (Hint: env vars from a `.env` file you don't commit.)

## Stretch
- **Use env vars for secrets**: move `POSTGRES_PASSWORD` and the Django `SECRET_KEY` to a `.env` file (referenced by `docker-compose.yml` with `env_file:`), and add `.env` to `.gitignore`.  Commit a `.env.example`.
- **Add nginx**: put an `nginx` container in front of `api` so traffic comes in on port 80 instead of 8000.  Map port 80 on the host and update the EC2 security group accordingly.
- **Add a healthcheck** to the `db` service and switch `depends_on` to `condition: service_healthy` so `run_compose.sh` doesn't need `sleep`.
- **Migrate on startup**: move `python manage.py migrate` into the api container's entrypoint so you don't need `run_compose.sh` at all.

> Stuck? Have a code error? Use the ["4 Before Me"](https://docs.google.com/document/d/1nseOs5oabYBKNHfwJZNAR7GlU0zkZxNagsw63AD7XV0/edit) debugging checklist to help you solve it!
