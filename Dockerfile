# Dockerfile
FROM python:3.7-stretch
EXPOSE 80
COPY . /app
WORKDIR /app
ENV PIP_CONFIG_FILE=/app/pip.conf
RUN pip install -r requirements.txt
ENTRYPOINT ["sh", "launch.sh"]