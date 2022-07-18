#!/bin/sh

if ["$DATABASE" = "postgres"]; then
    echo "Waiting for postgres..."
    
    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done
    
    echo "PostgreSQL started"
fi

echo >&2 "PostgreSQL is ready!"
echo $(pwd)
echo $(cd /usr/src/app && ls)
echo $(cd /usr/src/app && python manage.py makemigrations --no-input && python manage.py migrate --no-input)

exec "$@"