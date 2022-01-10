# pull official base image
FROM node:14-alpine3.14

# set work directory
WORKDIR /usr/src/app

# copy our react dependency files
COPY ./gui/package.json .
COPY ./gui/package-lock.json .

# install serve - deployment static server suggested by official create-react-app
RUN npm install -g serve

# install dependencies and avoid `node-gyp rebuild` errors
RUN apk add --virtual .gyp \
        python3 \
        make \
        g++ \
    && npm install \
    && apk del .gyp

# copy our react project
COPY ./gui .

RUN npm run build

CMD serve -s build -l 3000
