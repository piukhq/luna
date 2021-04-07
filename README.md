# Luna
Test helper, Mock project, Jeff.

## configurations

- create a `.env` file in the root directory
- add your configurations based on the environmental variables required in `app.settings.py`

## running

- `poetry install`
- `poetry run python wsgi.py`

## unittest
- `poetry run pytest tests --cov=app --cov-report=term-missing`
