FROM binkhq/python:3.9

WORKDIR /app
ADD . .
RUN pip install --no-cache-dir poetry gunicorn && \
    poetry config virtualenvs.create false && \
    poetry install

CMD [ "gunicorn", "--workers=2", "--threads=2", "--error-logfile=-", \
                  "--access-logfile=-", "--bind=0.0.0.0:9000", "wsgi:app" ]
