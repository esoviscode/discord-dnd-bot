# dockerfile 
FROM ubuntu:20.04
RUN apt -y update
RUN apt -y install python
RUN apt -y install pip
RUN pip install discord --no-input
