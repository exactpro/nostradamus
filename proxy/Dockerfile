FROM nginx:1.16-alpine
RUN apk add --no-cache bash \
&& apk add --no-cache curl \
&& apk add --no-cache busybox-extras
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/conf.d/* /etc/nginx/conf.d/
RUN mkdir -p /opt/nginx/certs
COPY proxy-entrypoint.sh .
ENTRYPOINT ["bash", "proxy-entrypoint.sh"]
