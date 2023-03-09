FROM python:3.9-slim
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y python3-dev default-libmysqlclient-dev build-essential
ENV PYTHONUNBUFFERED 1
RUN mkdir /marvel
WORKDIR /marvel

ADD requirements.txt /marvel/
RUN python -m pip install --upgrade pip
RUN pip install -r /marvel/requirements.txt
ADD . /marvel/