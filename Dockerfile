# Use python3.8 as base image
FROM python:3.8
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app

# Expose the port
EXPOSE 8000

# Run the application
CMD ["chalice", "local", "--host=0.0.0.0", "--port=8000"]