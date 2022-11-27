# dockerfile 
# syntax=docker/dockerfile:1

FROM python:3.11-alpine

RUN pip3 install discord

CMD [ "python3","main.py" ]
