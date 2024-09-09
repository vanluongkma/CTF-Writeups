FROM python:3.10

WORKDIR /app
COPY . /app

RUN apt update && apt install -y openssl socat && pip install pycryptodome
RUN apt install -y libsasl2-dev python-dev-is-python3 libldap2-dev libssl-dev
RUN pip install pyOpenSSL
RUN pip install secrets
RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
