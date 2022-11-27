# dockerfile 
FROM ubuntu:20.04
RUN apt -y update
RUN pip install discord --no-input
