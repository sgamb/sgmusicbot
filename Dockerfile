# syntax=docker/dockerfile:1
FROM python:3.10-slim
WORKDIR /bot
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
WORKDIR /bot/data
COPY data/foo.db .
WORKDIR /bot/src
COPY src/* ./
CMD ["python3", "app.py"]
