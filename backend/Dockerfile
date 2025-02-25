# pull official base image
FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENV=prod

# set work directory
WORKDIR /usr/backend

# copy requirements file
COPY ./requirements.txt /usr/backend/requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# copy project
COPY . /usr/backend/