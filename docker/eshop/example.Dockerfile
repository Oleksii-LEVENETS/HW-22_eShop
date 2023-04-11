FROM python:latest

ENV DOCKERIZE_VERSION=v0.6.1

# Copy only requirements, to cache them in docker layer:
WORKDIR /pysetup

COPY ./warehouse/requirements.txt /pysetup/

# Project initialization:
RUN pip install -r requirements.txt

# Installing `dockerize` utility:
# https://github.com/jwilder/dockerize
RUN wget "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && tar -C /usr/local/bin -xzvf "dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && rm "dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz"

# This is a special case. We need to run this script as an entry point:
COPY ./docker/warehouse/docker-entrypoint.sh ./docker/warehouse/wait-for-command.sh ./docker/warehouse/runserver.sh /
RUN chmod +x /docker-entrypoint.sh /wait-for-command.sh /runserver.sh

# This dir will become the mountpoint of development code:
WORKDIR /code

ENTRYPOINT ["/docker-entrypoint.sh"]
