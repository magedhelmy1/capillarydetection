To clean docker images and volumes from OS

    docker-compose down
    yes | docker image prune -a
    docker volume rm $(docker volume ls -q)