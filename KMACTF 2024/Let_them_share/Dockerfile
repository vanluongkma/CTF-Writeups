FROM python:3.10

WORKDIR /app
COPY . /app

RUN apt update && apt install -y socat && pip install pycryptodome

CMD socat TCP-L:2004,reuseaddr,fork EXEC:"python3 server.py"