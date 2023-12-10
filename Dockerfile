# Dockerfile
FROM python:3.9
EXPOSE 80
COPY . /app
WORKDIR /app
ENV PIP_CONFIG_FILE=/app/pip.conf
RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && apt-get -y install ffmpeg libsm6 libxext6 # required for pytesseract, opencv
RUN pip install -r requirements.txt
ENTRYPOINT ["sh", "launch.sh"]