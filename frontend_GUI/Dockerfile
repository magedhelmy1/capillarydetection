###########
# BUILDER #
###########

# pull official base image
FROM node:12.18.3-alpine3.9 as builder

# set work directory
WORKDIR /usr/src/app

# install dependencies and avoid `node-gyp rebuild` errors
COPY ./gui/package.json .
RUN apk add --no-cache --virtual .gyp \
        python \
        make \
        g++ \
    && npm install \
    && apk del .gyp

# copy our react project
COPY ./gui .

# perform npm build
RUN npm run build

#########
# FINAL #
#########

# pull official base image
FROM node:12.18.3-alpine3.9 

# set work directory
WORKDIR /usr/src/app

# copy entrypoint.sh
COPY ./entrypoint.prod.sh /usr/src/app/entrypoint.prod.sh

# install serve - deployment static server suggested by official create-react-app
RUN npm install -g serve

# copy our build files from our builder stage
COPY --from=builder /usr/src/app/build ./build

# run entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.prod.sh
ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]