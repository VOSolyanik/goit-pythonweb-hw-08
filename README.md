# goit-pythonweb-hw-08

## Setup

### 1. Install project dependencies

-  `poetry install`

### 2. Run local Postgres DB in Docker

- `docker run --name student-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres` where `mysecretpassword` is your custom password. Other params could be changed too.

### 3. Create .env file

- You need to create `.env` file from sample `.env.sample` and update according to your params in Docker command that runs Postgres instance

### 4. Run DB migrations

- `poetry run alembic upgrade head`

### 5. Run seeding (optional)

- `poetry run python seed.py` to fill DB with test data

### 6. Run

- `poetry run python -m main` and navigate to `http://127.0.0.1:8000/docs`

## Results:

- As the result we have a REST API app for managing `contacts`
- We have basic CRUD operations
- We have `api/contacts` api that supports `limit`, `offset` params, `search_text` parameter to find contact by `first_name`, `last_name` or `email`, and `upcoming_birthdays` parameter - if set to `true` filters users which have birth day in next 7 days.