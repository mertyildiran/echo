# Use an official Python runtime as a parent image
FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Maintainer
MAINTAINER Mehmet Mert Yıldıran "mert.yildiran@bil.omu.edu.tr"

# Install GDAL library
RUN apt-get update
RUN apt-get install -y gdal-bin python-gdal
RUN apt-get install -y --reinstall libspatialite7
RUN apt-get install -y libsqlite3-mod-spatialite

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install pip3
RUN apt-get install -y python3-pip

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Create the database
RUN python3 manage.py migrate

# Make port 80 available to the world outside this container
EXPOSE 80

# Start the app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]
