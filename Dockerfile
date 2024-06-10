# Base image
FROM python:3.12

# Set the working directory
WORKDIR /app


# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000


# Define environment variable
ENV NAME World

# Run app.py when the container launches chalice local
CMD ["chalice", "local", "--port", "8000"]
