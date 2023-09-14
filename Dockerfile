# Dockerfile
FROM python:3.7-stretch
EXPOSE 80
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt --trusted-host https://pypi.pkg.jetbrains.space/50gramx/p/main/python-delivery/simple
ENTRYPOINT ["sh", "eapp_identity_program.sh"]