# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /app

COPY ./dnd-bot/ .
# ADD ./dnd-bot/requirements.txt ./requirements.txt

RUN pip3 install -r ./requirements.txt


CMD [ "python3","-u","main.py" ]
