FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/"

WORKDIR /code/

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY . .
RUN chmod +x /code/entrypoint.sh

RUN poetry install --no-dev
