# syntax=docker/dockerfile:1

FROM python:3.8-slim

WORKDIR /bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR source

CMD ["python3", "musicbot.py"]
