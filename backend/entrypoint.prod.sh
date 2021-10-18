#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

(cd frontend && npm install && npm run prod)
python manage.py collectstatic --noinput

exec "$@"
