# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install discord


CMD [ "python3","dnd-bot/dnd_bot/main.py" ]
