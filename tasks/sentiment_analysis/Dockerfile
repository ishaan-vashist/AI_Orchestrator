FROM python:3.10-slim

WORKDIR /app
COPY app.py .

RUN pip install --no-cache-dir transformers torch

CMD ["python", "app.py"]
