FROM python:3.11.1

ENV PYTHONUNBUFFERED 1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /code

RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /code/

RUN poetry install

COPY . .
RUN poetry install
