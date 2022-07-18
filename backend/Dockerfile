# pull official base image
FROM python:3.9-slim-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app
RUN python -m pip install --upgrade pip

# installing netcat (nc) since we are using that to listen to postgres server in entrypoint
RUN apt-get update && apt-get install -y --no-install-recommends netcat && \
    apt-get install ffmpeg libsm6 libxext6 build-essential libpq-dev -y &&\
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy dependencies file
RUN pip install tensorflow-aarch64 -f https://tf.kmtea.eu/whl/stable.html
COPY requirementsLocal.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh /usr/src/entrypoint.sh

ENTRYPOINT ["sh","/usr/src/entrypoint.sh"]


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

