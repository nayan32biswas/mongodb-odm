FROM python:3.8

ENV PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
