FROM python:3.10.5

WORKDIR /app

COPY requirements.txt requirements.txt

COPY . /app

RUN pip install -r requirements.txt

ENV FLASK_APP=src.app:main_app