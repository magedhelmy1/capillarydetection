# pull official base image
FROM node:14-alpine3.14

# set work directory
WORKDIR /usr/src/app

# copy entrypoint.sh
COPY ./entrypoint.prod.sh /usr/src/app/entrypoint.prod.sh

# copy our react project
COPY ./gui .

# install serve - deployment static server suggested by official create-react-app
RUN npm install -g serve

# install dependencies and avoid `node-gyp rebuild` errors
RUN apk add --virtual .gyp \
        python3 \
        make \
        g++ \
    && npm install \
    && apk del .gyp

ARG REACT_APP_AXIOS_URL
ENV REACT_APP_AXIOS_URL=${REACT_APP_AXIOS_URL}
RUN npm run build

# run entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.prod.sh
ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]
