# Use an official Python runtime
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Expose the API port
EXPOSE 7676

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7676"]