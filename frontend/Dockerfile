FROM node:12.18.3-alpine3.9 as builder

# set work directory
WORKDIR /usr/src/app

# install dependencies and avoid `node-gyp rebuild` errors
COPY ./web_frontend/package.json .
RUN apk add --no-cache --virtual .gyp \
        python \
        make \
        g++ \
    && npm install \
    && apk del .gyp

# copy our react project
COPY ./web_frontend .

# perform npm build
ARG API_URL
ENV REACT_APP_AXIOS_URL=${API_URL}
RUN REACT_APP_AXIOS_URL=${API_URL} \
  npm run build

# pull official base image
FROM node:12.18.3-alpine3.9


# set work directory
WORKDIR /usr/src/app

# install serve - deployment static server suggested by official create-react-app
RUN npm install -g serve

# copy our build files from our builder stage
COPY --from=builder /usr/src/app/build ./build