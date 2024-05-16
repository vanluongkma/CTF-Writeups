FROM python:3.10
FROM node:latest

WORKDIR /app
COPY . /app

RUN apt update && apt install -y socat

CMD socat TCP-L:2005,reuseaddr,fork EXEC:"python3 server.py"