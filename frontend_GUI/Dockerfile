###########
# BUILDER #
###########

# pull official base image
#FROM node:14-alpine3.14 as builder
FROM node:14-alpine3.14

# set work directory
WORKDIR /usr/src/app

# install dependencies and avoid `node-gyp rebuild` errors
COPY ./gui/package.json .
RUN apk add --no-cache --virtual .gyp \
        python3 \
        make \
        g++ \
    && npm install \
    && apk del .gyp

# copy our react project
COPY ./gui .

# perform npm build
# perform npm build
ARG REACT_APP_AXIOS_URL
ENV REACT_APP_AXIOS_URL=${REACT_APP_AXIOS_URL}
RUN REACT_APP_AXIOS_URL=${REACT_APP_AXIOS_URL}
RUN npm run build
# install serve - deployment static server suggested by official create-react-app
RUN npm install -g serve

# copy entrypoint.sh
COPY ./entrypoint.prod.sh /usr/src/app/entrypoint.prod.sh

# run entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.prod.sh
ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]
