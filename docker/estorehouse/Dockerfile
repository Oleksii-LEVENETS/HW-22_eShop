# estorehouse/Dockerfile

# Base image
FROM python:3.9.6-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc postgresql-client libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install dependencies

RUN pip install --upgrade pip
COPY ./estorehouse/requirements.txt .
RUN pip install -r ./estorehouse/requirements.txt

# Copy entrypoint script
COPY ./docker/estorehouse/docker-entrypoint.sh /

# Copy wait-for-command script
COPY ./docker/estorehouse/wait-for-command.sh /

# Copy runserver script
COPY ./docker/estorehouse/runserver.sh /

# Copy application code
COPY . .

# Run entrypoint script
ENTRYPOINT ["/docker/estorehouse/docker-entrypoint.sh"]
