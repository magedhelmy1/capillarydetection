#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

python manage.py makemigrations --no-input
python manage.py flush --no-input
python manage.py migrate
(cd frontend && npm install && npm run dev)
python manage.py collectstatic --no-input

if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser \
    --noinput \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL \
    --password $DJANGO_SUPERUSER_PASSWORD
fi
exec "$@"
