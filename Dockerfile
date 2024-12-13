FROM amd64/ubuntu:22.04

RUN groupadd -g 1000 python && \
    useradd -r -u 1000 -g python python

RUN mkdir /app && chown python:python /app
WORKDIR /app
RUN apt update 
RUN apt install -y python3 python3-pip iproute2
RUN pip install --force-reinstall python-telegram-bot
COPY mycredencials.py .
COPY smtp2telegram.py .

USER 1000
CMD ["python3", "smtp2telegram.py"]
