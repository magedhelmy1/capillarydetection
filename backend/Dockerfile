# pull the official base image
FROM python:3.8.12-bullseye
RUN --mount=type=cache,target=/root/.cache/pip

# set work directory
WORKDIR /usr/src/app

# copy project
COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update \
    && apt-get install ffmpeg libsm6 libxext6  -y \
    && apt-get install -y curl \
    && curl --silent --location https://deb.nodesource.com/setup_12.x | bash - \
    && apt-get install -y nodejs \
    && npm install --silent\
    && npm install react-scripts@3.4.1 -g --silent

RUN apt install -y netcat
COPY /requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# set work directory
WORKDIR /usr/src/app

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
