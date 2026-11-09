# ─── stage 1: builder ───
FROM python:3.11-slim AS builder
WORKDIR /build

COPY requirements.txt ./
RUN pip install --no-cache-dir uv \
    && uv venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH
RUN uv pip install --no-cache -r requirements.txt

# ─── stage 2: runtime ───
FROM python:3.11-slim
WORKDIR /app

RUN groupadd -r app && \
    useradd -r -g app -d /app app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app . /app

RUN chmod +x /app/entrypoint.sh

ENV VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1

USER app
EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
