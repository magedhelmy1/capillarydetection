## To clean docker images and volumes from OS

    docker-compose down
    yes | docker image prune -a
    docker volume rm $(docker volume ls -q)

## To do performance testing:

    locust -f performanceTesting\load_testing.py
    go to -> http://localhost:8089/

## To check celery queuing:

    go to -> http://localhost:5556/dashboard

## Purpose:

- This is a simple program where the user has a frontend with 21 samples of capillary images, or the user can upload
  their own image.
- The image is taken to the backend, analyzed with deep learning and the analyzed image is back along with the segmented
  image and the original image.

## Structure:

The structure is demonstrated below from the Docker-files, you also have access via Gi To build locally:

- docker-compose up -d –-build
- Open in browser at http://localhost
- Change the code and see code updating
- To add new backend migrations:

To rebuild locally:

- docker-compose down --volume --rmi all
- docker-compose up -d –build

## Deployment:

The server is deployed on Digital Ocean for no special reason, should be deployable anywhere. The website accessible
on http://64.227.106.224/

## CI/CD:

- pushing to the repo main automatically triggers a deploy to  http://64.227.106.224/, so if you will push, please push
  to a branch you have created locally.

## Development setup

During development all the code files are mounted into containers. This allows file watchers to work and to be able to
hot-reload when changing the code.

**NOTE:** When changing dependencies docker images need to be rebuilt.

Django:

- Docker image only installs dependencies
- Code is mounted into the container from the host machine
- Sample env file for development is provided
- To add new migrations use `docker-compose run --rm web python manage.py makemigrations --no-input`

React:

- Docker image only installs system dependencies
- Code and node_modules are mounted directly in to the container
- When container starts it installs dependencies to be able to save time during development when adding extra packages

