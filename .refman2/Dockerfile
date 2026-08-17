FROM ubuntu:22.04

# Avoid prompts during the install
ENV DEBIAN_FRONTEND=noninteractive  
RUN apt-get update

RUN apt-get update && apt-get install -y \
  wget \
  python3 \
  python3-pip \
  python3-dev \ 
  build-essential \ 
  sqlite3 \
  zathura 

COPY ./requirements.txt .
RUN pip install -r requirements.txt


