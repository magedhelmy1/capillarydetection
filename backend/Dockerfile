# pull the official base image
FROM python:3.8.12-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

# install dependencies
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY /requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy project
COPY .. /usr/src/app

# EXPOSE 8000

WORKDIR /usr/src/app/backend

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


