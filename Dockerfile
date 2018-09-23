# Pull base image
FROM python:3-alpine

MAINTAINER jmhansen@fastmail.com

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set working directory
RUN mkdir /code
WORKDIR /code

# Copy contents of current directory into working directory
ADD . /code/

# install pipenv and install Python packages
RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["python", "app/main.py"]
