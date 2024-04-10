# Dockerfile
FROM python:3.9
EXPOSE 80
RUN apt-get update && apt-get -y upgrade \
  && apt-get -y install tesseract-ocr \
  && apt-get -y install ffmpeg libsm6 libxext6 \
  && apt-get -y install poppler-utils # required for pytesseract, opencv, pdf2image
COPY ./requirements.txt /app/requirements.txt
COPY ./pip.conf /app/pip.conf
ENV PIP_CONFIG_FILE=/app/pip.conf
RUN pip install -r /app/requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["sh", "launch.sh"]