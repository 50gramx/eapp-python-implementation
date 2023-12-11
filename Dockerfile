# Dockerfile
FROM python:3.9
EXPOSE 80
RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && apt-get -y install ffmpeg libsm6 libxext6 # required for pytesseract, opencv
COPY ./requirements.txt /app/requirements.txt
COPY ./pip.conf /app/pip.conf
ENV PIP_CONFIG_FILE=/app/pip.conf
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["sh", "launch.sh"]