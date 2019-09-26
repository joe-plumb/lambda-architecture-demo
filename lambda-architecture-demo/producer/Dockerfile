# Use an official Python runtime as a parent image
FROM python:3.7-slim

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make ports available to the world outside this container
EXPOSE 5000
EXPOSE 5671
EXPOSE 5672
EXPOSE 443

# Run app.py when the container launches
CMD ["python", "app.py"]