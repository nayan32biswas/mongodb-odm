FROM python:3.11

ENV PIP_DEFAULT_TIMEOUT=100

RUN pip install "poetry==1.7.1"

WORKDIR /code
COPY pyproject.toml *.lock /code/

RUN poetry config virtualenvs.create false \
    &&  poetry install --no-interaction --no-ansi

COPY . .
