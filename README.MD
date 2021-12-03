**To clean docker images and volumes from OS**

    docker-compose down
    yes | docker image prune -a
    docker volume rm $(docker volume ls -q)


**To do performance testing:**

    locust -f performanceTesting\load_testing.py
    go to -> http://localhost:8089/

**To check celery queuing:**

    go to -> http://localhost:5556/dashboard

**Purpose:**

 - This is a simple program where the user has a frontend with 21 samples of capillary images, or the user can upload their own image.
- The image is taken to the backend, analyzed with deep learning and the analyzed image is back along with the segmented image and the original image.

**Structure:**

The structure is demonstrated below from the Docker-files, you also have access via Gi
To build locally:
-	docker-compose up -d –build
To rebuild locally, after doing changes – first do the following:
-	docker-compose down --volume --rmi all
-	docker-compose up -d –build

**Deployment:** 
The server is deployed on Digital Ocean for no special reason, should be deployable anywhere.
The website accessible on http://64.227.106.224/

**CI/CD:**
-	pushing to the repo main automatically triggers a deploy to  http://64.227.106.224/, so if you will push, please push to a branch you have created locally.


