## Scope:
The contents of this project are at the interface between deep learning, image processing, early detection of diseases,
and clinical practice.

## Novelty:

The proposed method is unique as it combines traditional image processing methods with neural network-based ones,
striking a balance between speed of processing and accuracy.

## Clinical Use:

The methodology of the paper bears direct clinical significance and has already been applied to patients suffering from
Covid-19, besides other diseases. Thus, it is highly relevant and of paramount importance to current society, even from
a practical perspective.

## Research Papers:

Details of the capillary algorithm can be found by the same authors in a paper titled:
[_CapillaryNet: An Automated System to Quantify Skin Capillary Density and Red Blood Cell Velocity from Handheld Vital
Microscopy_](https://arxiv.org/abs/2104.11574)


## Build Project Locally

Clone the repo and run the following command or navigate to URL http://www.analysecapillary.space/

     docker-compose up -d –-build

## To rebuild locally:

      docker-compose down --volume --rmi all
      docker-compose down &&  docker-compose up -d --build

## Performance testing:

    locust -f performanceTesting\load_testing.py --master

Usually, a performance server can support up to 500 RPS.
The more workers are spawned, the more RPS can be created.

    locust -f performanceTesting\load_testing.py --worker
    http://localhost:8089/

Our server can process up to 3000 RPS per second.

## To check celery queuing:

    http://localhost:5556/dashboard

## CI/CD:

- On merge, a deploy is triggered to http://139.59.206.141/, which is redirects to URL http://www.analysecapillary.space/

## Development setup

During development, all the code files are mounted into containers. This allows file watchers to work and to be able to
hot-reload when changing the code.

**NOTE:** When changing dependencies, Docker images need to be rebuilt.

Django:

- Docker image only installs dependencies
- Code is mounted into the container from the host machine
- Sample env file for development is provided
- To add new migrations use

      docker-compose run --rm web python manage.py makemigrations --no-input

React:

- Docker image only installs system dependencies
- Code and node_modules are mounted directly into the container
- When the container starts it installs dependencies to be able to save time during development when adding extra packages

## Project Structure:

* algorithms_HSV: This folder contains one folder and one file. The folder includes the Keras algorithm and the docker file of the algorithm that copies the algorithm to the docker container.
* algorithms_SSIM: This folder contains one folder and one file. The folder includes the Keras algorithm and the docker file that copies the algorithm to the docker container.
* backend:
    * Dockerfile and Dockerfile.prod: Create docker containers during local build or production build, respectively.
    * entrypoint.sh and entrypoint.prod.sh: Creates entry point shell file during local build or production build
      , respectively. These files are called from the docker files mentioned above
    * requirements.txt: Contains the requirement needed to build the backend. This file is called from the docker file
    * Backend_apps: This is where the backend files are
        * manage.py: starts the server
        * .env.sample: sample variables to be used for local build
        * templates: contains a simple HTML to inspect if Redis is receiving calls and generating a task id
        * Server: contains all the server dedicated files
            * celery.py: contains celery configuration
            * settings.py: contains the settings for the server
            * contains the URL for the server
            * asgi.py and wsgi.py: auto-generated files, but the server uses the wsgi.py file
            * image_classifier:
                * migration_folder: auto-generated but needed by the backend
                * API folder: contains the communication protocols between the server and the GUI
                    * serializers: serializes the backend
                    * URLs: contains the GET and POST URL between the server and the GUI
                    * views: contains the script of how the API should behave when a GET and POST request is generated
                * admin.py: registers the backend model
                * algorithm_v2.py: contains the script relevant to the deep learning part. This file uses the
                  algorithms_HSV and algorithms_SSIM folder
                * apps.py: metadata for the database
                * models.py: contains the table for the database
                * tasks.py: contains the algorithm_v1 script. This is currently not in use but kept for reference.
                * views.py: contains the ASGI script to communicate with the Sasgi part of the server. his is currently
                  not in use but kept for reference
* diagram: contains the paper diagram
* frontend_GUI:
    * Dockerfile and Dockerfile.prod: Create docker containers during local build or production build, respectively.
    * GUI folder: contains all the frontend related folders and files
        * src: contains the folders that are needed to edit the frontend
            * components: Contains all the files needed to edit the frontend
            * Static Media: contains the 24 sample images used in the frontend
            * *.css, *.js: styling and colors of the frontend
        * public: auto-generated folder, the only modification is under index.html to use the correct frontend bootstrap
        * package.json and package-lock.json: auto-generated and contains metadata about the GUI, which is required
          before publishing to NPM
* Nginx:
    * Dockerfile and Dockerfile.prod: Creates docker containers during local build or in production build, respectively.
    * README.md: contains the configuration used in the frontend
    * nginx**.conf: contains the routing rules and protocols between the frontend, api and the backend

* performance testing
    * workers.sh: contains the configuration for testing the performance
    * load_testing.py: the script to test the RPS of the server
* .docker-compose.yaml: Builds the whole project locally; errors are shown in the local console.
* .docker-compose.ci.yml: Builds the project in the continuous integration pipeline. Errors are shown
  in [Github Actions](https://github.com/magedhelmy1/capillarydetection/actions).
* .docker-compose.prod.yml: Builds the project in the continuous integration pipeline. Errors are shown
  in [Github Actions](https://github.com/magedhelmy1/capillarydetection/actions).

## Contributing:

We love your input! You can contribute to the project the following way:

- Bug Reporting
- Submitting a fix
- Propose new feature(s)
- Becoming a maintainer

Read more in our [contributing.md](https://github.com/magedhelmy1/capillarydetection/blob/master/contributing.md) file


