FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip3 install --upgrade pip setuptools && pip3 install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "backend.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
