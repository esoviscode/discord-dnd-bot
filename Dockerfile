# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN pip3 install discord

CMD [ "python3","main.py" ]
