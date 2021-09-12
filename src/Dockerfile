FROM python:3.9.0-slim-buster
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src
COPY . /src/

RUN apt-get update
RUN apt-get install -y build-essential python-gdal libpq-dev git cmake locales gettext

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000