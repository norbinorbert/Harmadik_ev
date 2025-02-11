FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install pika
CMD ["python3", "consumer_producer.py"]
