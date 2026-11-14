#
# Sample docker Nginx image
# More info: https://hub.docker.com/_/nginx/
#
FROM nginx:1.30.6-alpine

# Expose Nginx HTTP service
EXPOSE 80 443

RUN mkdir /logs
COPY services/nginx/nginx.conf /etc/nginx/
COPY services/nginx/openfisca-djangoapi.conf /etc/nginx/sites-enabled/
