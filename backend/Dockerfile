# pull official base image
FROM python:3.9-slim-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

# installing netcat (nc) since we are using that to listen to postgres server in entrypoint
RUN apt-get update && apt-get install -y --no-install-recommends netcat && \
    apt-get install ffmpeg libsm6 libxext6 build-essential -y &&\
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy dependencies file
COPY requirements.txt .
RUN pip install -r requirements.txt
#RUN pip install -U 'Twisted[tls,http2]'

COPY entrypoint.sh /usr/src/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["sh","/usr/src/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
