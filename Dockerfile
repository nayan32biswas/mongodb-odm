FROM python:3.9

ENV PYTHONUNBUFFERED=1 \
    UV_REQUESTS_TIMEOUT=100 \
    UV_SYSTEM_PYTHON=1 \
    UV_LINK_MODE=copy

RUN curl -LsSf https://astral.sh/uv/0.6.10/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /code

ADD . /code

RUN uv sync --extra dev
