# Dockerfile
FROM python:3.7-stretch
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
COPY ../../wiki/eapp-wiki/config/environment/microservices/eapp-identity.dev.env /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["sh", "eapp_identity_program.sh"]