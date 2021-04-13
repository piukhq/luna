FROM binkhq/python:3.9

WORKDIR /app
ADD . .
RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy --ignore-pipfile

CMD [ "gunicorn", "--workers=2", "--threads=2", "--error-logfile=-", \
    "--access-logfile=-", "--bind=0.0.0.0:9000", "wsgi:app" ]
