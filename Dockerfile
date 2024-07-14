# Use the Python 3.9 base image
FROM python:3.9

# Expose ports for the application
EXPOSE 80
EXPOSE 443   
EXPOSE 8000
EXPOSE 8080

# Update the package list and upgrade all packages
RUN apt-get update && apt-get -y upgrade \
  # Install Tesseract OCR
  && apt-get -y install tesseract-ocr \
  # Install FFmpeg and required libraries for OpenCV
  && apt-get -y install ffmpeg libsm6 libxext6 \
  # Install Poppler utilities for PDF processing
  && apt-get -y install poppler-utils

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Copy the pip configuration file into the container
COPY ./pip.conf /app/pip.conf

# Copy the Nginx configuration file into the container
COPY nginx.conf /app/nginx/nginx.conf

# Set environment variables for SSL certificates
ENV SSL_CERT /app/certificates/server.crt
ENV SSL_KEY /app/certificates/server.key

# Copy SSL certificates and key into the container image
COPY certificates/server.crt /app/certificates/server.crt
COPY certificates/server.key /app/certificates/server.key

# Set the pip configuration file environment variable
ENV PIP_CONFIG_FILE=/app/pip.conf

# Install the Python dependencies from the requirements file
RUN pip install -r /app/requirements.txt

# Copy the application code into the container
COPY . /app

# Set the working directory inside the container
WORKDIR /app

# Set the entry point to the launch script
ENTRYPOINT ["sh", "launch.sh"]
