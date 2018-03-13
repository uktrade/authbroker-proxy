FROM nginx:latest

RUN apt-get update && apt-get install openssl

COPY default.conf /etc/nginx/conf.d/
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

CMD /entrypoint.sh

