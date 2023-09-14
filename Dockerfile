# Dockerfile
FROM python:3.7-stretch
EXPOSE 50501
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt --trusted-host https://pypi.pkg.jetbrains.space/50gramx/p/main/python-delivery/simple
ENTRYPOINT ["sh", "eapp_identity_program.sh"]