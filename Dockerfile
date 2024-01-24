FROM python:3.8

RUN pip install "poetry"

WORKDIR /code
COPY pyproject.toml *.lock /code/

RUN poetry config virtualenvs.create false \
    &&  poetry install --no-interaction --no-ansi

COPY . .
