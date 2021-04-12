# Luna
Test helper, Mock project, Jeff.

## configurations

- make a .env file from the provided example `cp .env.example .env`
- modify your configurations based on the environmental variables required in `app.settings.py`

## running

- `poetry install`
- `poetry run python wsgi.py`

## unittest
- `poetry run pytest tests --cov=app --cov-report=term-missing`
