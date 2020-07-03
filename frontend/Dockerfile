###########
# BUILDER #
###########

# build environment
FROM node:13.12.0-alpine as build
WORKDIR /src/app
ENV PATH /src/app/node_modules/.bin:$PATH
COPY package.json ./
RUN npm i --silent && npm install react-scripts@3.4.1 -g --silent
COPY . ./
RUN npm run build

#########
# FINAL #
#########

# production environment
FROM nginx:1.16-alpine
RUN apk add --no-cache bash
RUN apk add --no-cache curl
RUN apk add --no-cache busybox-extras
COPY --from=build /src/app/build /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/conf.d/* /etc/nginx/conf.d/
RUN mkdir -p /opt/nginx/certs
COPY frontend-entrypoint.sh .
ENTRYPOINT ["bash", "frontend-entrypoint.sh"]
