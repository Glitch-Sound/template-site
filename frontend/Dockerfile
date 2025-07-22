FROM node:20-slim

ENV TZ=Asia/Tokyo

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/package*.json ./
RUN npm install --legacy-peer-deps

COPY app/ .

RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 5173
