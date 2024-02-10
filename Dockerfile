FROM ghcr.io/binkhq/python:3.10
ARG PIP_INDEX_URL
ARG APP_NAME
ARG APP_VERSION
WORKDIR /app
ADD wsgi.py .
RUN pip install --no-cache ${APP_NAME}==$(echo ${APP_VERSION} | cut -c 2-)

ENV PROMETHEUS_MULTIPROC_DIR=/dev/shm
CMD [ "gunicorn", "--error-logfile=-", "--access-logfile=-", "--bind=0.0.0.0:9000", "wsgi:app" ]
