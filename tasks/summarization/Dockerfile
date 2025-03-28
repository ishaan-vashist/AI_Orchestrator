FROM python:3.10-slim

RUN pip install transformers torch

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
