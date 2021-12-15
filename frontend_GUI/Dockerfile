# pull official base image
FROM node:14-alpine3.14

# set work directory
WORKDIR /usr/src/app

# install dependencies and avoid `node-gyp rebuild` errors
RUN apk add \
        bash \
        python3 \
        make \
        g++

CMD /bin/bash -c "npm install && npm run start"
