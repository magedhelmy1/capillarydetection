#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

python manage.py makemigrations --no-input
python manage.py migrate
python manage.py collectstatic --noinput
(cd frontend && touch .env && echo "REACT_APP_AXIOS_URL=http://"$REACT_APP_AXIOS_URL"" >.env && npm install && npm run prod)
exec "$@"
