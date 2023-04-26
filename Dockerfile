FROM python:buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt update

# for installation dependencies with pip
# COPY ./requirements.txt ./
# RUN pip3 install --upgrade pip --no-cache-dir && pip3 install -r requirements.txt --no-cache-dir

COPY ./poetry.lock ./pyproject.toml /code/

RUN pip install --upgrade pip
RUN pip install poetry

# Install project dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --only main
