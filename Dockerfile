# Dockerfile
FROM python:3.9
EXPOSE 80
COPY . /app
WORKDIR /app
ENV PIP_CONFIG_FILE=/app/pip.conf
RUN apt install tesseract-ocr
RUN pip install -r requirements.txt
ENTRYPOINT ["sh", "launch.sh"]