FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --shell /usr/sbin/nologin scanner

WORKDIR /app
COPY sosmed_scanner/ ./sosmed_scanner/

USER scanner
ENTRYPOINT ["python", "-m", "sosmed_scanner.cli"]