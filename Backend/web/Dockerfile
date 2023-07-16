FROM python:3.10

COPY . /app
WORKDIR /app

RUN pip install poetry==1.4.2 && \
    pip install python-multipart
RUN poetry export -o requirements.txt && \
    pip install -r requirements.txt 

CMD ["python", "app.py"]