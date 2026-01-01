FROM node:20.19-alpine

ENV TZ=Asia/Tokyo

RUN apk add --no-cache build-base

WORKDIR /app

COPY app/package*.json ./
RUN npm install --legacy-peer-deps

COPY app/ .

RUN chown -R node:node /app

USER node

EXPOSE 5173
