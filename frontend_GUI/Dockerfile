# pull official base image
FROM node:14-alpine3.14

# set work directory
WORKDIR /usr/src/app

# copy our react dependency files
COPY ./gui/package.json .
COPY ./gui/package-lock.json ./


RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

# install dependencies and avoid `node-gyp rebuild` errors
RUN apk add --virtual .gyp \
        python3 \
        make \
        g++ \
        && npm install \
        && apk del .gyp



# copy our react project
COPY ./gui .

CMD ["npm", "start"]






