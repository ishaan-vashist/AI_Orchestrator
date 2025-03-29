# Use lightweight Python 3.10 image to minimize container size
FROM python:3.10-slim

# Install required libraries for Hugging Face pipeline
RUN pip install transformers torch

# Set the working directory inside the container
WORKDIR /app

# Copy the summarization script into the container
COPY app.py .

# Run the summarization task when the container starts
CMD ["python", "app.py"]
