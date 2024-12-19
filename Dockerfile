FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get clean

# Install Python packages
RUN pip install --no-cache-dir \
    ultralytics \
    opencv-python-headless \
    vidgear \
    flask \
    flask-cors \
    requests

# Copy your application code
WORKDIR /app
COPY . /app

# Expose port for Flask
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
