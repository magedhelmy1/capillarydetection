## Scope:
The contents of this project are at the interface between deep learning, 
image processing, early detection of diseases, 
and clinical practice.

## Novelty:
The proposed method is unique as it combines traditional image 
processing methods with neural network-based ones, 
striking a balance between speed of processing and accuracy.

## Clinical Use:
The methodology of the paper bears direct clinical significance 
and has already been applied to patients suffering from Covid-19, 
besides other diseases. 
Thus, it is highly relevant and of paramount importance to 
current society, even from a practical perspective.

## Research Papers:
Details of the capillary algorithm can be found by the same authors in a paper titled -> _CapillaryNet: An Automated System to Quantify Skin Capillary Density and Red Blood Cell Velocity from Handheld Vital Microscopy_


## Build Project Locally

Clone repo and run the following command or navigate to URL http://www.analysecapillary.space/

     docker-compose up -d –-build

## To rebuild locally:

      docker-compose down --volume --rmi all
      docker-compose down &&  docker-compose up -d --build

## Performance testing:

    locust -f performanceTesting\load_testing.py --master

Usually a performance server can support up to 500 RPS.
The more workers are spawned, the more RPS can be created.

    locust -f performanceTesting\load_testing.py --worker 
    http://localhost:8089/

Our server can process up to 3000 RPS per second

## To check celery queuing:

    http://localhost:5556/dashboard

## CI/CD:

- On merge, a deploy is triggered to http://139.59.206.141/ which is redirects to URL http://www.analysecapillary.space/

## Development setup

During development all the code files are mounted into containers. This allows file watchers to work and to be able to
hot-reload when changing the code.

**NOTE:** When changing dependencies docker images need to be rebuilt.

Django:

- Docker image only installs dependencies
- Code is mounted into the container from the host machine
- Sample env file for development is provided
- To add new migrations use

      docker-compose run --rm web python manage.py makemigrations --no-input

React:

- Docker image only installs system dependencies
- Code and node_modules are mounted directly in to the container
- When container starts it installs dependencies to be able to save time during development when adding extra packages
