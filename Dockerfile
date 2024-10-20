# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set environment variables to prevent __pycache__ directories
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /youtube_data_fetch

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /youtube_data_fetch/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY ./youtube_data_fetch /youtube_data_fetch

# Set the path to the virtual environment
ENV PATH="/py/bin:$PATH"
