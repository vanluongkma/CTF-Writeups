FROM sagemath/sagemath:latest

USER root

RUN apt-get -qq update \
    && apt-get -qq install -y --no-install-recommends \
    netcat \
    tmux \
    vim \
    xinetd \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /ctf
WORKDIR /ctf

RUN echo "Connection blocked" > /etc/banner_fail
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY ./source /ctf/

RUN chmod -R 750 /ctf && \
    chmod 740 /ctf/flag.txt 

ENTRYPOINT []
CMD ["/usr/sbin/xinetd", "-dontfork"]

EXPOSE 9999