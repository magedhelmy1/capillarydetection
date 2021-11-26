#!/bin/sh

cd frontend
touch .env
echo "REACT_APP_AXIOS_URL=http://"$REACT_APP_AXIOS_URL"" >.env

exec "$@"
