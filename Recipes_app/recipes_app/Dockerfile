FROM python:3.10-alpine3.18

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt /temp/requirements.txt
COPY recipes_app /recipes_app
WORKDIR /recipes_app
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt