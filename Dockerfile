# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /

# Copy the entire current directory into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirement.txt

# Expose the port that FastAPI will run on (optional if using -p in docker run command)
EXPOSE ${PORT}

# Command to run Redis and FastAPI application when the container starts
CMD redis-server & uvicorn main:app --host 0.0.0.0 --port ${PORT}
