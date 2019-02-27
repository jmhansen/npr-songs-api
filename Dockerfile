# Pull base image
FROM python:3.6

MAINTAINER jmhansen@fastmail.com

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set working directory
RUN mkdir /src
WORKDIR /src

# Copy contents of current directory into working directory
ADD . /src/

# install pipenv and install Python packages
RUN pip install pipenv
RUN pipenv install --deploy --python=`which python3`

ENV FLASK_ENV=docker
EXPOSE 5000