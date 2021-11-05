#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

(cd frontend && touch .env && echo "REACT_APP_AXIOS_URL=http://"$REACT_APP_AXIOS_URL"" > .env && npm install && npm run prod && python manage.py makemigrations && python manage.py flush --no-input && python manage.py migrate && python manage.py collectstatic --noinput)
exec "$@"
