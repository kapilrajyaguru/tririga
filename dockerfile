# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port used by the Flask app
EXPOSE 8080

# Start the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
