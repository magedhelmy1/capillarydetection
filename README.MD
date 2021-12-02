To clean docker images and volumes from OS

    docker-compose down
    yes | docker image prune -a
    docker volume rm $(docker volume ls -q)


To do performance testing:

    locust -f performanceTesting\load_testing.py
    go to -> http://localhost:8089/

To check celery queuing:

    go to -> http://localhost:5556/dashboard
