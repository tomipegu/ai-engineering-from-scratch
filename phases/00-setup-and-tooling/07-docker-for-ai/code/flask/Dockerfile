# Use a lightweight Python 3.12 base image
FROM python:3.12-slim

# Make Python print logs immediately instead of buffering them
ENV PYTHONUNBUFFERED=1

# Set /app as the working directory inside the container
WORKDIR /app

# Upgrade pip, then install Flask and the Qdrant Python client
RUN python -m pip install --no-cache-dir \
    --upgrade pip \
    && python -m pip install --no-cache-dir \
    flask \
    qdrant-client

# Copy the Flask application into the container
COPY app.py /app/app.py

# Document that the application listens on port 5000
EXPOSE 5000

# Start the Flask application when the container starts
CMD ["python", "/app/app.py"]