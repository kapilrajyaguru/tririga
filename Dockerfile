# Use official Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Change ownership and set permissions for OpenShift's non-root user
RUN chown -R 1001:0 /app && chmod -R 775 /app

# Allow group permissions (required by OpenShift)
USER 1001

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8080

# Start the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
