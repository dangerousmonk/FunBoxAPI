# syntax=docker/dockerfile:1
FROM python:3.8.5
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
