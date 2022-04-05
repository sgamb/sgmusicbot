# syntax=docker/dockerfile:1
FROM python:3.8-slim
WORKDIR /bot
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY *.py ./
COPY *.db .
CMD ["python3", "musicbot.py"]
