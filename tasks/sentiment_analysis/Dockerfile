# Use slim Python 3.10 base image to keep container lightweight
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy task script into the container
COPY app.py .

# Install only required libraries (no cache to reduce image size)
RUN pip install --no-cache-dir transformers torch

# Run the sentiment analysis script by default
CMD ["python", "app.py"]
