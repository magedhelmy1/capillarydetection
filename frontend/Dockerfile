FROM node:14.4.0-alpine3.10
USER root
WORKDIR /frontend/web_frontend
COPY . /frontend/web_frontend
ARG API_URL
ENV REACT_APP_HOST_IP_ADDRESS $API_URL
RUN yarn
RUN yarn build