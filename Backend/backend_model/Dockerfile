From python:3.10

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY . /app
WORKDIR /app/app

RUN pip install poetry==1.4.2
RUN poetry install

EXPOSE 8080
CMD poetry run uvicorn main:app --host 0.0.0.0 --port 8080